from __future__ import annotations

import discord

from ..signals.models import SignalResult


def signal_embed(signal: SignalResult) -> discord.Embed:
    color = discord.Color.green() if signal.direction == "bullish" else discord.Color.red()
    title = f"{signal.symbol} {signal.direction.upper()} breakout"
    embed = discord.Embed(title=title, color=color)
    embed.add_field(name="Price", value=f"{signal.price:.2f}")
    embed.add_field(name="Level", value=f"{signal.level:.2f}")
    embed.add_field(name="Note", value=signal.note, inline=False)
    return embed


def status_message(tickers: list[str]) -> str:
    if not tickers:
        return "No tickers are currently being monitored."
    return "Currently monitoring: " + ", ".join(tickers)
