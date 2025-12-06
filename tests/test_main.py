import asyncio

import pytest

pytest.importorskip("httpx")

from src.config import Config
from src.bot.client import SupportResistanceBot
from src.data.providers.coingecko import CoinGeckoProvider
from src.main import build_provider


def base_config(**overrides):
    return Config(
        discord_token="token",
        discord_channel_id=1,
        tickers=["BTC"],
        **overrides,
    )


def test_build_provider_coingecko():
    provider = build_provider(base_config())
    assert isinstance(provider, CoinGeckoProvider)


def test_build_provider_unknown():
    cfg = base_config(market_data_provider="unknown")
    with pytest.raises(ValueError):
        build_provider(cfg)


class DummyManager:
    tickers: list[str]

    def __init__(self) -> None:
        self.tickers = []

    async def evaluate_all(self):  # pragma: no cover - trivial async
        return []


@pytest.mark.asyncio
async def test_bot_enables_message_content_intent():
    bot = SupportResistanceBot(
        signal_manager=DummyManager(),
        channel_id=1,
        command_prefix="!",
    )
    try:
        assert bot.intents.message_content is True
    finally:
        await bot.close()


@pytest.mark.asyncio
async def test_bot_close_cancels_poll_task():
    bot = SupportResistanceBot(
        signal_manager=DummyManager(),
        channel_id=1,
        command_prefix="!",
    )
    poll_task = asyncio.create_task(asyncio.sleep(1))
    bot._task = poll_task
    await bot.close()
    assert poll_task.cancelled()
