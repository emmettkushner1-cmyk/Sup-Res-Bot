from datetime import datetime, timezone, timedelta

from src.signals.support_resistance import calculate_levels, detect_breakout
from src.signals.models import Candle


def make_candle(price: float, high: float | None = None, low: float | None = None, ts_offset: int = 0) -> Candle:
    now = datetime(2024, 1, 1, tzinfo=timezone.utc) + timedelta(minutes=ts_offset)
    return Candle(
        timestamp=now,
        open=price,
        high=high if high is not None else price,
        low=low if low is not None else price,
        close=price,
    )


def test_calculate_levels_identifies_pivots():
    candles = [
        make_candle(100, high=101, low=99, ts_offset=0),
        make_candle(102, high=103, low=101, ts_offset=1),
        make_candle(99, high=100, low=98, ts_offset=2),
        make_candle(104, high=105, low=103, ts_offset=3),
        make_candle(101, high=102, low=100, ts_offset=4),
    ]
    levels = calculate_levels(candles, lookback=1)
    assert 105 in levels.resistances
    assert 98 in levels.supports


def test_detect_breakout_flags_bullish_move():
    candles = [
        make_candle(100, high=101, low=99, ts_offset=0),
        make_candle(102, high=103, low=101, ts_offset=1),
        make_candle(99, high=100, low=98, ts_offset=2),
        make_candle(104, high=105, low=103, ts_offset=3),
        make_candle(110, high=111, low=109, ts_offset=4),
    ]
    signal = detect_breakout("BTC", candles, buffer_ratio=0.001)
    assert signal.breakout is True
    assert signal.direction == "bullish"
    assert signal.level == 105
