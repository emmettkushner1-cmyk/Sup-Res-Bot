from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List


class StateStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def load_tickers(self) -> List[str]:
        if not self.path.exists():
            return []
        with self.path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data.get("tickers", [])

    def save_tickers(self, tickers: Iterable[str]) -> None:
        payload: Dict[str, Any] = {"tickers": list(tickers)}
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2)
