from pathlib import Path

from src.config import Config


def test_config_from_env(monkeypatch):
    monkeypatch.setenv("DISCORD_TOKEN", "token")
    monkeypatch.setenv("DISCORD_CHANNEL_ID", "123")
    monkeypatch.setenv("TICKERS", "BTC,ETH")
    monkeypatch.setenv("POLL_INTERVAL", "30")
    cfg = Config.from_env()

    assert cfg.discord_token == "token"
    assert cfg.discord_channel_id == 123
    assert cfg.tickers == ["BTC", "ETH"]
    assert cfg.poll_interval == 30
    assert cfg.state_file == Path("state.json")
