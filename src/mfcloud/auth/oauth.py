"""OAuth 2.0 authorization-code flow for Money Forward's ID platform.

The Accounting API supports ONLY this flow (no API keys). Tokens are office-scoped:
whichever office the user picks on Money Forward's consent screen is the office the
token can access — hence one profile per office.

Login runs a loopback listener on http://127.0.0.1:<port>/callback (the redirect URI
registered in the App Portal), opens the browser, and exchanges the returned code.
PKCE (S256) and a random state are always sent. The confidential client secret is
presented via HTTP Basic auth first (client_secret_basic); on a 401 the request is
retried once with the credentials in the form body (client_secret_post), so both
App Portal client-authentication-method registrations work without configuration.
"""

from __future__ import annotations

import base64
import hashlib
import http.server
import secrets
import threading
import time
import urllib.parse
import webbrowser
from dataclasses import dataclass

import httpx

from mfcloud.auth.store import TokenSet, TokenStore
from mfcloud.errors import APIErrorDetail, MFCAuthError, parse_oauth_error_details

AUTHORIZE_URL = "https://api.biz.moneyforward.com/authorize"
TOKEN_URL = "https://api.biz.moneyforward.com/token"

ALL_SCOPES = [
    "mfc/accounting/offices.read",
    "mfc/accounting/accounts.read",
    "mfc/accounting/departments.read",
    "mfc/accounting/journal.read",
    "mfc/accounting/journal.write",
    "mfc/accounting/voucher.write",
    "mfc/accounting/report.read",
    "mfc/accounting/taxes.read",
    "mfc/accounting/trade_partners.read",
    "mfc/accounting/trade_partners.write",
    "mfc/accounting/connected_account.read",
    "mfc/accounting/transaction.read",
    "mfc/accounting/transaction.write",
]


@dataclass
class PKCEPair:
    verifier: str
    challenge: str

    @classmethod
    def generate(cls) -> PKCEPair:
        verifier = secrets.token_urlsafe(64)[:128]
        digest = hashlib.sha256(verifier.encode("ascii")).digest()
        challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
        return cls(verifier=verifier, challenge=challenge)


def build_authorize_url(
    client_id: str,
    redirect_uri: str,
    state: str,
    code_challenge: str,
    scopes: list[str] | None = None,
) -> str:
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": " ".join(scopes or ALL_SCOPES),
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    return f"{AUTHORIZE_URL}?{urllib.parse.urlencode(params)}"


def parse_callback(url: str, expected_state: str) -> str:
    """Extract the authorization code from a redirect URL, verifying state."""
    query = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
    if "error" in query:
        description = (query.get("error_description") or [""])[0]
        raise ValueError(f"Authorization failed: {query['error'][0]} {description}".strip())
    state = (query.get("state") or [""])[0]
    if state != expected_state:
        raise ValueError("OAuth state mismatch — possible CSRF; aborting login.")
    code = (query.get("code") or [""])[0]
    if not code:
        raise ValueError("No authorization code in callback URL.")
    return code


def exchange_code(
    client_id: str,
    client_secret: str,
    code: str,
    redirect_uri: str,
    code_verifier: str,
    http_client: httpx.Client | None = None,
) -> dict:
    return _token_request(
        client_id,
        client_secret,
        {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "code_verifier": code_verifier,
        },
        http_client,
    )


def refresh_grant(
    client_id: str,
    client_secret: str,
    refresh_token: str,
    http_client: httpx.Client | None = None,
) -> dict:
    return _token_request(
        client_id,
        client_secret,
        {"grant_type": "refresh_token", "refresh_token": refresh_token},
        http_client,
    )


def _token_request(
    client_id: str,
    client_secret: str,
    data: dict,
    http_client: httpx.Client | None,
) -> dict:
    """POST a grant to the token endpoint.

    Client auth is client_secret_basic first; a 401 means the app is registered
    with client_secret_post, so retry once with credentials in the body. A rejected
    client-auth attempt does not consume the authorization code, so the retry is
    safe. Fallback happens only on 401 — a 400 (invalid_grant etc.) means client
    auth already succeeded and retrying cannot help.
    """
    client = http_client or httpx.Client(timeout=30.0)
    try:
        response = client.post(TOKEN_URL, data=data, auth=(client_id, client_secret))
        if response.status_code == 401:
            response = client.post(
                TOKEN_URL,
                data={**data, "client_id": client_id, "client_secret": client_secret},
            )
        if response.status_code >= 400:
            raise MFCAuthError(
                status=response.status_code,
                details=parse_oauth_error_details(response),
            )
        return response.json()
    finally:
        if http_client is None:
            client.close()


class _CallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 (stdlib API name)
        self.server.callback_path = self.path  # type: ignore[attr-defined]
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(
            b"<html><body><h2>Login complete</h2>"
            b"<p>You can close this tab and return to the terminal.</p></body></html>"
        )

    def log_message(self, *args) -> None:
        pass


def receive_callback(port: int, timeout: float = 300.0) -> str:
    """Serve one loopback request and return the full callback path."""
    server = http.server.HTTPServer(("127.0.0.1", port), _CallbackHandler)
    server.timeout = timeout
    server.callback_path = None  # type: ignore[attr-defined]
    try:
        while server.callback_path is None:  # type: ignore[attr-defined]
            server.handle_request()
        return server.callback_path  # type: ignore[attr-defined]
    finally:
        server.server_close()


def login(
    client_id: str,
    client_secret: str,
    port: int,
    scopes: list[str] | None = None,
    manual: bool = False,
    http_client: httpx.Client | None = None,
    open_browser=webbrowser.open,
    prompt=input,
    clock=time.time,
) -> TokenSet:
    """Run the full authorization-code flow and return a TokenSet."""
    redirect_uri = f"http://127.0.0.1:{port}/callback"
    state = secrets.token_urlsafe(24)
    pkce = PKCEPair.generate()
    url = build_authorize_url(client_id, redirect_uri, state, pkce.challenge, scopes)
    if manual:
        print(f"Open this URL in your browser:\n\n{url}\n")
        callback = prompt("Paste the full redirect URL you were sent to: ").strip()
    else:
        print("Opening browser for Money Forward login...")
        open_browser(url)
        callback = receive_callback(port)
    code = parse_callback(callback, state)
    data = exchange_code(client_id, client_secret, code, redirect_uri, pkce.verifier, http_client)
    return TokenSet.from_token_response(data, now=clock())


class TokenManager:
    """Hands out a valid access token, refreshing proactively and on demand."""

    def __init__(
        self,
        store: TokenStore,
        profile: str,
        client_id: str,
        client_secret: str,
        http_client: httpx.Client | None = None,
        clock=time.time,
    ) -> None:
        self._store = store
        self._profile = profile
        self._client_id = client_id
        self._client_secret = client_secret
        self._http = http_client
        self._clock = clock
        self._lock = threading.Lock()

    def get_access_token(self) -> str:
        with self._lock:
            tokens = self._require_tokens()
            if tokens.expiring(self._clock()):
                tokens = self._refresh(tokens)
            return tokens.access_token

    def force_refresh(self) -> str:
        with self._lock:
            return self._refresh(self._require_tokens()).access_token

    def _require_tokens(self) -> TokenSet:
        tokens = self._store.load_tokens(self._profile)
        if tokens is None:
            raise MFCAuthError(
                status=0,
                details=[
                    APIErrorDetail(
                        code="not_logged_in",
                        message=(
                            f"No stored tokens for profile '{self._profile}'."
                            " Run `mfc auth login` first."
                        ),
                    )
                ],
            )
        return tokens

    def _refresh(self, tokens: TokenSet) -> TokenSet:
        data = refresh_grant(
            self._client_id, self._client_secret, tokens.refresh_token, self._http
        )
        fresh = TokenSet.from_token_response(data, now=self._clock())
        if not fresh.refresh_token:
            fresh.refresh_token = tokens.refresh_token
        self._store.save_tokens(self._profile, fresh)
        return fresh


class BearerAuth(httpx.Auth):
    """Injects the bearer token; on 401, refreshes once and retries the request."""

    def __init__(self, manager: TokenManager) -> None:
        self._manager = manager

    def auth_flow(self, request: httpx.Request):
        request.headers["Authorization"] = f"Bearer {self._manager.get_access_token()}"
        response = yield request
        if response.status_code == 401:
            request.headers["Authorization"] = f"Bearer {self._manager.force_refresh()}"
            yield request
