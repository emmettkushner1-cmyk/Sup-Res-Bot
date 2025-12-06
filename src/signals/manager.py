from __future__ import annotations

import logging
from typing import Dict, Iterable, List

from .support_resistance import detect_breakout
from .models import SignalResult
from ..data.providers.base import MarketDataProvider
from ..data.cache import TTLCache
from ..utils.errors import DataFetchError, SignalError


class SignalManager:
    def __init__(
        self,
        provider: MarketDataProvider,
        tickers: Iterable[str],
        dedupe_seconds: int = 300,
        logger: logging.Logger | None = None,
    ) -> None:
        self.provider = provider
        self.tickers = list(tickers)
        self.logger = logger or logging.getLogger(__name__)
        self.last_alerts: TTLCache[str, str] = TTLCache(ttl_seconds=dedupe_seconds, max_entries=512)

    async def evaluate_all(self) -> List[SignalResult]:
        signals: List[SignalResult] = []
        for symbol in self.tickers:
            try:
                signal = await self.evaluate_symbol(symbol)
            except DataFetchError as exc:
                self.logger.warning("Data fetch error for %s: %s", symbol, exc)
                continue
            except SignalError as exc:
                self.logger.error("Signal error for %s: %s", symbol, exc)
                continue
            if signal.breakout and self._is_new_alert(symbol, signal.direction):
                signals.append(signal)
        return signals

    async def evaluate_symbol(self, symbol: str) -> SignalResult:
        candles = await self.provider.get_ohlcv(symbol, limit=30)
        try:
            signal = detect_breakout(symbol, candles)
        except Exception as exc:  # noqa: BLE001
            raise SignalError(str(exc)) from exc
        return signal

    def _is_new_alert(self, symbol: str, direction: str) -> bool:
        last_direction = self.last_alerts.get(symbol)
        if last_direction == direction:
            return False
        self.last_alerts.set(symbol, direction)
        return True
