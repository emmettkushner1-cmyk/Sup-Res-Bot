from __future__ import annotations

import asyncio
import logging
from typing import Optional

import discord
from discord.ext import commands

from ..signals.manager import SignalManager
from .commands import register_commands
from .formatting import signal_embed


class SupportResistanceBot(commands.Bot):
    def __init__(
        self,
        signal_manager: SignalManager,
        channel_id: int,
        poll_interval: float = 10.0,
        *args,
        **kwargs,
    ) -> None:
        intents = kwargs.pop("intents", discord.Intents.default())
        intents.message_content = True
        super().__init__(*args, intents=intents, **kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.signal_manager = signal_manager
        self.channel_id = channel_id
        self.poll_interval = poll_interval
        self._task: Optional[asyncio.Task] = None
        register_commands(self, signal_manager)

    async def setup_hook(self) -> None:
        self._task = asyncio.create_task(self._poll_signals())

    async def on_ready(self) -> None:
        self.logger.info("Logged in as %s", self.user)

    async def close(self) -> None:
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        await super().close()

    async def _poll_signals(self) -> None:
        await self.wait_until_ready()
        while not self.is_closed():
            try:
                signals = await self.signal_manager.evaluate_all()
                if signals:
                    channel = self.get_channel(self.channel_id)
                    if channel is None:
                        self.logger.warning("Channel %s not found", self.channel_id)
                    else:
                        for signal in signals:
                            await channel.send(embed=signal_embed(signal))
            except asyncio.CancelledError:
                break
            except Exception as exc:  # noqa: BLE001
                self.logger.exception("Error polling signals: %s", exc)
            await asyncio.sleep(self.poll_interval)
