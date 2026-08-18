"""`mfc auth login` credential handling — no browser, no network, fake keyring."""

import pytest
from typer.testing import CliRunner

from mfcloud.auth.store import TokenSet, TokenStore
from mfcloud.cli import auth_cmd
from mfcloud.cli.app import app
from mfcloud.config import Config
from tests.unit.test_auth import FakeKeyring

runner = CliRunner()


@pytest.fixture
def env(monkeypatch, tmp_path):
    """Isolated config + keyring + stubbed OAuth flow."""
    config = Config(client_id="cid", path=tmp_path / "config.toml")
    store = TokenStore(backend=FakeKeyring())
    logins = []

    def fake_login(client_id, secret, port, manual=False):
        logins.append({"client_id": client_id, "secret": secret})
        return TokenSet("at", "rt", expires_at=9e9)

    monkeypatch.setattr(auth_cmd.Config, "load", classmethod(lambda cls: config))
    monkeypatch.setattr(auth_cmd, "TokenStore", lambda: store)
    monkeypatch.setattr(auth_cmd, "oauth_login", fake_login)
    return store, logins


def test_login_prompts_for_secret_with_hidden_input(env):
    store, logins = env
    result = runner.invoke(app, ["auth", "login"], input="shh-secret\n")
    assert result.exit_code == 0, result.output
    assert "input hidden" in result.output
    assert "shh-secret" not in result.output  # hidden input is not echoed
    assert store.load_client_secret() == "shh-secret"
    assert logins[0]["secret"] == "shh-secret"


def test_login_reuses_stored_secret_without_prompt(env):
    store, logins = env
    store.save_client_secret("already-there")
    result = runner.invoke(app, ["auth", "login"])
    assert result.exit_code == 0, result.output
    assert "Client Secret" not in result.output
    assert logins[0]["secret"] == "already-there"


def test_login_strips_pasted_whitespace_from_secret(env):
    store, logins = env
    result = runner.invoke(app, ["auth", "login"], input=" s3cret \n")
    assert result.exit_code == 0, result.output
    assert store.load_client_secret() == "s3cret"
    assert logins[0]["secret"] == "s3cret"


def test_login_flag_still_accepted(env):
    store, logins = env
    result = runner.invoke(app, ["auth", "login", "--client-secret", "via-flag"])
    assert result.exit_code == 0, result.output
    assert store.load_client_secret() == "via-flag"
