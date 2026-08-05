from mfcloud.config import Config


def test_load_missing_file_gives_defaults(tmp_path, monkeypatch):
    monkeypatch.delenv("MFC_CLIENT_ID", raising=False)
    config = Config.load(tmp_path / "config.toml")
    assert config.client_id == ""
    assert config.redirect_port == 8730
    assert config.default_profile == "default"


def test_save_and_reload_roundtrip(tmp_path, monkeypatch):
    monkeypatch.delenv("MFC_CLIENT_ID", raising=False)
    monkeypatch.delenv("MFC_REDIRECT_PORT", raising=False)
    path = tmp_path / "config.toml"
    Config(client_id="abc123", redirect_port=9999, default_profile="tokyo", path=path).save()
    config = Config.load(path)
    assert config.client_id == "abc123"
    assert config.redirect_port == 9999
    assert config.default_profile == "tokyo"


def test_env_overrides_file(tmp_path, monkeypatch):
    path = tmp_path / "config.toml"
    Config(client_id="from-file", path=path).save()
    monkeypatch.setenv("MFC_CLIENT_ID", "from-env")
    assert Config.load(path).client_id == "from-env"


def test_resolve_profile_precedence(monkeypatch):
    config = Config(default_profile="default")
    monkeypatch.delenv("MFC_PROFILE", raising=False)
    assert config.resolve_profile() == "default"
    monkeypatch.setenv("MFC_PROFILE", "env-office")
    assert config.resolve_profile() == "env-office"
    assert config.resolve_profile("explicit") == "explicit"
