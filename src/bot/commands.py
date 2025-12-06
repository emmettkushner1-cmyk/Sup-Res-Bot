from __future__ import annotations

import discord
from discord.ext import commands

from ..signals.manager import SignalManager
from .formatting import status_message


def register_commands(bot: commands.Bot, manager: SignalManager) -> None:
    @bot.command(name="tickers")
    async def list_tickers(ctx: commands.Context) -> None:
        await ctx.send(status_message(manager.tickers))

    @bot.command(name="add")
    async def add_ticker(ctx: commands.Context, symbol: str) -> None:
        if symbol not in manager.tickers:
            manager.tickers.append(symbol)
            await ctx.send(f"Added {symbol} to watchlist")
        else:
            await ctx.send(f"{symbol} is already being monitored")

    @bot.command(name="remove")
    async def remove_ticker(ctx: commands.Context, symbol: str) -> None:
        if symbol in manager.tickers:
            manager.tickers.remove(symbol)
            await ctx.send(f"Removed {symbol}")
        else:
            await ctx.send(f"{symbol} was not being monitored")

    @bot.command(name="health")
    async def health(ctx: commands.Context) -> None:
        await ctx.send("Bot is online and monitoring signals")
