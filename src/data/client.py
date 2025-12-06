from __future__ import annotations

import asyncio
from typing import Any, Dict, Optional

import httpx

DEFAULT_TIMEOUT = 10.0
DEFAULT_MAX_RETRIES = 3
DEFAULT_BACKOFF = 0.5


class AsyncHTTPClient:
    def __init__(
        self,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        backoff: float = DEFAULT_BACKOFF,
    ) -> None:
        self._client = httpx.AsyncClient(timeout=timeout)
        self.max_retries = max_retries
        self.backoff = backoff

    async def get(self, url: str, params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        for attempt in range(1, self.max_retries + 2):
            try:
                response = await self._client.get(url, params=params)
                response.raise_for_status()
                return response
            except (httpx.RequestError, httpx.HTTPStatusError):
                if attempt > self.max_retries:
                    raise
                await asyncio.sleep(self.backoff * attempt)
        raise RuntimeError("Exceeded retry attempts")

    async def aclose(self) -> None:
        await self._client.aclose()
