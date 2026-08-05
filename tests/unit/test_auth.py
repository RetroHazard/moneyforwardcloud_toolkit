"""OAuth flow tests — fake keyring, mocked token endpoint, no browser, no network."""

import threading

import httpx
import pytest

from mfcloud.auth.oauth import (
    ALL_SCOPES,
    TOKEN_URL,
    BearerAuth,
    PKCEPair,
    TokenManager,
    build_authorize_url,
    login,
    parse_callback,
    receive_callback,
)
from mfcloud.auth.store import TokenSet, TokenStore
from mfcloud.errors import MFCAuthError


class FakeKeyring:
    def __init__(self):
        self.data = {}

    def set_password(self, service, name, value):
        self.data[(service, name)] = value

    def get_password(self, service, name):
        return self.data.get((service, name))

    def delete_password(self, service, name):
        del self.data[(service, name)]


@pytest.fixture
def store():
    return TokenStore(backend=FakeKeyring())


def token_endpoint(responses: list[dict]):
    """Mock httpx client acting as the token endpoint, serving canned responses."""
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        assert str(request.url) == TOKEN_URL
        calls.append(dict(httpx.QueryParams(request.content.decode())))
        return httpx.Response(200, json=responses[len(calls) - 1])

    return httpx.Client(transport=httpx.MockTransport(handler)), calls


# --- store ---------------------------------------------------------------------


def test_token_store_roundtrip(store):
    tokens = TokenSet("acc", "ref", 12345.0, ["a.read"])
    store.save_tokens("default", tokens)
    assert store.load_tokens("default") == tokens
    store.delete_tokens("default")
    assert store.load_tokens("default") is None


def test_client_secret_roundtrip(store):
    store.save_client_secret("shh")
    assert store.load_client_secret() == "shh"


def test_token_set_expiry():
    tokens = TokenSet.from_token_response(
        {"access_token": "a", "refresh_token": "r", "expires_in": 3600, "scope": "x y"},
        now=1000.0,
    )
    assert tokens.expires_at == 4600.0
    assert tokens.scopes == ["x", "y"]
    assert not tokens.expiring(now=4500.0)
    assert tokens.expiring(now=4545.0)  # inside 60s margin


# --- authorize URL / callback --------------------------------------------------


def test_authorize_url_contents():
    url = build_authorize_url("cid", "http://127.0.0.1:8730/callback", "st4te", "ch4llenge")
    assert url.startswith("https://api.biz.moneyforward.com/authorize?")
    assert "response_type=code" in url
    assert "client_id=cid" in url
    assert "state=st4te" in url
    assert "code_challenge=ch4llenge" in url
    assert "code_challenge_method=S256" in url
    assert "mfc%2Faccounting%2Fjournal.write" in url


def test_parse_callback_happy_path():
    assert parse_callback("/callback?code=abc&state=xyz", "xyz") == "abc"


def test_parse_callback_state_mismatch():
    with pytest.raises(ValueError, match="state mismatch"):
        parse_callback("/callback?code=abc&state=evil", "xyz")


def test_parse_callback_provider_error():
    with pytest.raises(ValueError, match="access_denied"):
        parse_callback("/callback?error=access_denied&state=xyz", "xyz")


def test_pkce_challenge_is_s256_of_verifier():
    import base64
    import hashlib

    pair = PKCEPair.generate()
    expected = base64.urlsafe_b64encode(
        hashlib.sha256(pair.verifier.encode()).digest()
    ).rstrip(b"=").decode()
    assert pair.challenge == expected


# --- full login flow (loopback server exercised over a real localhost socket) --


def test_login_loopback_flow():
    client, calls = token_endpoint(
        [{"access_token": "at", "refresh_token": "rt", "expires_in": 3600}]
    )
    port = 18731
    captured_url = {}

    def fake_browser(url):
        captured_url["url"] = url
        # Simulate the provider redirecting the user's browser to our loopback.
        state = dict(httpx.QueryParams(url.split("?", 1)[1]))["state"]

        def hit():
            httpx.get(f"http://127.0.0.1:{port}/callback?code=thecode&state={state}")

        threading.Thread(target=hit, daemon=True).start()

    tokens = login(
        "cid", "secret", port, http_client=client, open_browser=fake_browser, clock=lambda: 1000.0
    )
    assert tokens.access_token == "at"
    assert calls[0]["grant_type"] == "authorization_code"
    assert calls[0]["code"] == "thecode"
    assert calls[0]["code_verifier"]
    assert "scope=" in captured_url["url"]


def test_login_manual_flow():
    client, calls = token_endpoint(
        [{"access_token": "at", "refresh_token": "rt", "expires_in": 3600}]
    )
    prompts = {}

    def fake_prompt(message):
        # The state is embedded in the printed URL; recover it from the closure below.
        return prompts["redirect"]

    def fake_browser(url):
        raise AssertionError("manual mode must not open a browser")

    # Wrap login to capture the state from the URL it prints.
    import builtins

    real_print = builtins.print
    try:

        def capture_print(*args, **kwargs):
            for a in args:
                if isinstance(a, str) and "authorize?" in a:
                    state = dict(httpx.QueryParams(a.split("?", 1)[1]))["state"]
                    prompts["redirect"] = f"http://x/callback?code=c2&state={state}"
            real_print(*args, **kwargs)

        builtins.print = capture_print
        tokens = login(
            "cid", "secret", 8730, manual=True,
            http_client=client, open_browser=fake_browser, prompt=fake_prompt,
            clock=lambda: 0.0,
        )
    finally:
        builtins.print = real_print
    assert tokens.access_token == "at"
    assert calls[0]["code"] == "c2"


# --- token manager / bearer auth ----------------------------------------------


def test_manager_returns_valid_token_without_refresh(store):
    store.save_tokens("p", TokenSet("acc", "ref", expires_at=10_000.0))
    manager = TokenManager(store, "p", "cid", "sec", clock=lambda: 1000.0)
    assert manager.get_access_token() == "acc"


def test_manager_refreshes_expiring_token(store):
    client, calls = token_endpoint(
        [{"access_token": "new", "refresh_token": "newref", "expires_in": 3600}]
    )
    store.save_tokens("p", TokenSet("old", "oldref", expires_at=1030.0))
    manager = TokenManager(store, "p", "cid", "sec", http_client=client, clock=lambda: 1000.0)
    assert manager.get_access_token() == "new"
    assert calls[0]["grant_type"] == "refresh_token"
    assert calls[0]["refresh_token"] == "oldref"
    assert store.load_tokens("p").refresh_token == "newref"


def test_manager_keeps_old_refresh_token_if_none_returned(store):
    client, _ = token_endpoint([{"access_token": "new", "expires_in": 3600}])
    store.save_tokens("p", TokenSet("old", "keepme", expires_at=0.0))
    manager = TokenManager(store, "p", "cid", "sec", http_client=client, clock=lambda: 1000.0)
    manager.get_access_token()
    assert store.load_tokens("p").refresh_token == "keepme"


def test_manager_raises_when_not_logged_in(store):
    manager = TokenManager(store, "ghost", "cid", "sec")
    with pytest.raises(MFCAuthError, match="not_logged_in"):
        manager.get_access_token()


def test_bearer_auth_retries_once_on_401(store):
    token_client, _ = token_endpoint(
        [{"access_token": "fresh", "refresh_token": "r2", "expires_in": 3600}]
    )
    store.save_tokens("p", TokenSet("stale", "r1", expires_at=99_999.0))
    manager = TokenManager(store, "p", "cid", "sec", http_client=token_client, clock=lambda: 0.0)

    seen_tokens = []

    def api_handler(request: httpx.Request) -> httpx.Response:
        seen_tokens.append(request.headers["Authorization"])
        if request.headers["Authorization"] == "Bearer stale":
            return httpx.Response(401, json={"errors": []})
        return httpx.Response(200, json={"ok": True})

    api = httpx.Client(transport=httpx.MockTransport(api_handler), auth=BearerAuth(manager))
    response = api.get("https://api.test/x")
    assert response.status_code == 200
    assert seen_tokens == ["Bearer stale", "Bearer fresh"]


def test_all_scopes_count():
    assert len(ALL_SCOPES) == 13


def test_receive_callback_returns_path():
    port = 18732
    result = {}

    def serve():
        result["path"] = receive_callback(port)

    thread = threading.Thread(target=serve, daemon=True)
    thread.start()
    import time as _time

    for _ in range(50):
        try:
            httpx.get(f"http://127.0.0.1:{port}/callback?code=z&state=s")
            break
        except httpx.TransportError:
            _time.sleep(0.05)
    thread.join(timeout=5)
    assert result["path"] == "/callback?code=z&state=s"
