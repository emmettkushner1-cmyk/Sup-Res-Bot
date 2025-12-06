from __future__ import annotations

import importlib.util
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

_ENV_FILE = os.getenv("ENV_FILE")

if importlib.util.find_spec("dotenv"):
    from dotenv import load_dotenv as _load_dotenv

    def load_dotenv() -> None:
        if _ENV_FILE:
            _load_dotenv(_ENV_FILE)
        else:
            _load_dotenv()
else:  # pragma: no cover - fallback when dependency not installed
    def load_dotenv(*_args, **_kwargs) -> None:  # type: ignore[no-untyped-def]
        return None

load_dotenv()


@dataclass
class Config:
    discord_token: str
    discord_channel_id: int
    tickers: List[str] = field(default_factory=list)
    poll_interval: int = 60
    market_data_provider: str = "coingecko"
    log_level: str = "INFO"
    cache_ttl_seconds: int = 120
    cache_max_entries: int = 256
    state_file: Path = Path("state.json")

    @classmethod
    def from_env(cls) -> "Config":
        token = os.getenv("DISCORD_TOKEN")
        channel_id_raw = os.getenv("DISCORD_CHANNEL_ID")
        if not token:
            raise ValueError("DISCORD_TOKEN is required")
        if not channel_id_raw:
            raise ValueError("DISCORD_CHANNEL_ID is required")

        tickers_raw = os.getenv("TICKERS", "")
        tickers = [ticker.strip() for ticker in tickers_raw.split(",") if ticker.strip()]

        poll_interval = _int_env("POLL_INTERVAL", default=60, minimum=5)
        cache_ttl = _int_env("CACHE_TTL_SECONDS", default=120, minimum=10)
        cache_max = _int_env("CACHE_MAX_ENTRIES", default=256, minimum=1)

        state_file = Path(os.getenv("STATE_FILE", "state.json"))

        return cls(
            discord_token=token,
            discord_channel_id=int(channel_id_raw),
            tickers=tickers,
            poll_interval=poll_interval,
            market_data_provider=os.getenv("MARKET_DATA_PROVIDER", "coingecko"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            cache_ttl_seconds=cache_ttl,
            cache_max_entries=cache_max,
            state_file=state_file,
        )


def _int_env(name: str, default: int, minimum: Optional[int] = None) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(f"Environment variable {name} must be an integer") from exc
    if minimum is not None and value < minimum:
        raise ValueError(f"Environment variable {name} must be >= {minimum}")
    return value
