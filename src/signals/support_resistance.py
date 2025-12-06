from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .models import Candle, SignalResult


@dataclass
class SupportResistanceLevels:
    supports: List[float]
    resistances: List[float]


def _pivot_high(candles: List[Candle], idx: int, lookback: int) -> bool:
    if idx < lookback:
        return False
    current = candles[idx].high
    history = candles[idx - lookback : idx]
    return all(current >= candle.high for candle in history)


def _pivot_low(candles: List[Candle], idx: int, lookback: int) -> bool:
    if idx < lookback:
        return False
    current = candles[idx].low
    history = candles[idx - lookback : idx]
    return all(current <= candle.low for candle in history)


def calculate_levels(candles: List[Candle], lookback: int = 2) -> SupportResistanceLevels:
    supports: List[float] = []
    resistances: List[float] = []
    # skip the latest candle so we only use historical pivots
    for idx in range(lookback, len(candles) - 1):
        if _pivot_high(candles, idx, lookback):
            resistances.append(candles[idx].high)
        if _pivot_low(candles, idx, lookback):
            supports.append(candles[idx].low)
    # Deduplicate approximate levels by rounding
    supports = sorted(set(round(level, 2) for level in supports))
    resistances = sorted(set(round(level, 2) for level in resistances))
    return SupportResistanceLevels(supports=supports, resistances=resistances)


def detect_breakout(
    symbol: str,
    candles: List[Candle],
    buffer_ratio: float = 0.002,
) -> SignalResult:
    if len(candles) < 3:
        raise ValueError("At least 3 candles are required to detect breakouts")

    levels = calculate_levels(candles)
    last_close = candles[-1].close
    resistance = levels.resistances[-1] if levels.resistances else None
    support = levels.supports[0] if levels.supports else None

    breakout = False
    direction = "neutral"
    level = 0.0
    note = "No breakout detected"

    if resistance and last_close > resistance * (1 + buffer_ratio):
        breakout = True
        direction = "bullish"
        level = resistance
        note = f"Price closed above resistance {resistance}"  # noqa: E501
    elif support and last_close < support * (1 - buffer_ratio):
        breakout = True
        direction = "bearish"
        level = support
        note = f"Price closed below support {support}"  # noqa: E501

    return SignalResult(
        symbol=symbol,
        breakout=breakout,
        level=level,
        direction=direction,
        price=last_close,
        note=note,
    )
