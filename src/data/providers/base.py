from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, List

from ...signals.models import Candle


class MarketDataProvider(ABC):
    @abstractmethod
    async def get_latest_price(self, symbol: str) -> float:
        ...

    @abstractmethod
    async def get_ohlcv(self, symbol: str, limit: int = 50) -> List[Candle]:
        ...

    async def close(self) -> None:
        return None
