from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Iterable, List, Sequence


def utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


def rolling_windows(sequence: Sequence, window_size: int) -> Iterable[Sequence]:
    if window_size <= 0:
        raise ValueError("window_size must be positive")
    for idx in range(len(sequence) - window_size + 1):
        yield sequence[idx : idx + window_size]


def within_last(dt: datetime, delta: timedelta) -> bool:
    return utc_now() - dt <= delta


def as_timezone(dt: datetime, tz: timezone) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc).astimezone(tz)
    return dt.astimezone(tz)
