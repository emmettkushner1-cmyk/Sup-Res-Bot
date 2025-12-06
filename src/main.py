from __future__ import annotations

import asyncio
import logging
import sys

import discord

from .bot.client import SupportResistanceBot
from .config import Config
from .data.providers.base import MarketDataProvider
from .data.providers.coingecko import CoinGeckoProvider
from .logging_config import configure_logging
from .signals.manager import SignalManager
from .storage.state import StateStore


async def main() -> None:
    try:
        config = Config.from_env()
    except Exception as exc:  # noqa: BLE001
        print(f"Failed to load configuration: {exc}", file=sys.stderr)
        raise

    logger = configure_logging(config, __name__)

    provider = build_provider(config)
    state_store = StateStore(config.state_file)
    tickers = state_store.load_tickers() or config.tickers
    manager = SignalManager(
        provider=provider,
        tickers=tickers,
        dedupe_seconds=config.cache_ttl_seconds,
        logger=logger,
    )

    intents = discord.Intents.default()
    intents.message_content = True
    bot = SupportResistanceBot(
        command_prefix="!",
        intents=intents,
        signal_manager=manager,
        channel_id=config.discord_channel_id,
        poll_interval=config.poll_interval,
    )

    try:
        await bot.start(config.discord_token)
    finally:
        await provider.close()
        state_store.save_tickers(manager.tickers)


def build_provider(config: Config) -> MarketDataProvider:
    provider_name = config.market_data_provider.lower()
    if provider_name == "coingecko":
        return CoinGeckoProvider()
    raise ValueError(f"Unsupported market data provider: {config.market_data_provider}")


def run() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    run()
