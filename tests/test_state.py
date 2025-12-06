from pathlib import Path

from src.storage.state import StateStore


def test_save_tickers_creates_parent_dirs(tmp_path: Path):
    state_file = tmp_path / "nested" / "state.json"
    store = StateStore(state_file)

    store.save_tickers(["BTC", "ETH"])

    assert state_file.exists()
    assert state_file.read_text()
    assert store.load_tickers() == ["BTC", "ETH"]
