from __future__ import annotations

from datetime import datetime, timezone
from typing import List

from ..client import AsyncHTTPClient
from ..providers.base import MarketDataProvider
from ...signals.models import Candle
from ...utils.errors import DataFetchError


class CoinGeckoProvider(MarketDataProvider):
    BASE_URL = "https://api.coingecko.com/api/v3"

    def __init__(self, client: AsyncHTTPClient | None = None) -> None:
        self.client = client or AsyncHTTPClient()

    async def get_latest_price(self, symbol: str) -> float:
        endpoint = f"{self.BASE_URL}/simple/price"
        params = {"ids": symbol.lower(), "vs_currencies": "usd"}
        try:
            response = await self.client.get(endpoint, params=params)
        except Exception as exc:  # httpx errors already handled in client
            raise DataFetchError(str(exc)) from exc
        payload = response.json()
        try:
            return float(payload[symbol.lower()]["usd"])
        except Exception as exc:  # noqa: BLE001
            raise DataFetchError(f"Unexpected response shape for symbol {symbol}") from exc

    async def get_ohlcv(self, symbol: str, limit: int = 50) -> List[Candle]:
        # CoinGecko supports OHLC for 1/7/14/30/90/180/365/max days; pick minimal >= limit via 1-day interval.
        endpoint = f"{self.BASE_URL}/coins/{symbol.lower()}/ohlc"
        params = {"vs_currency": "usd", "days": 1}
        try:
            response = await self.client.get(endpoint, params=params)
        except Exception as exc:  # noqa: BLE001
            raise DataFetchError(str(exc)) from exc
        data = response.json()
        candles: List[Candle] = []
        for entry in data[:limit]:
            ts, open_p, high_p, low_p, close_p = entry
            candles.append(
                Candle(
                    timestamp=datetime.fromtimestamp(ts / 1000, tz=timezone.utc),
                    open=float(open_p),
                    high=float(high_p),
                    low=float(low_p),
                    close=float(close_p),
                    volume=None,
                )
            )
        if not candles:
            raise DataFetchError(f"No OHLCV data returned for symbol {symbol}")
        return candles

    async def close(self) -> None:
        await self.client.aclose()
