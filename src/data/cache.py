from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Generic, Optional, Tuple, TypeVar

from ..utils.time_windows import utc_now

K = TypeVar("K")
V = TypeVar("V")


timestamped_value = Tuple[datetime, V]


@dataclass
class CacheEntry(Generic[V]):
    value: V
    timestamp: datetime


class TTLCache(Generic[K, V]):
    def __init__(self, ttl_seconds: int, max_entries: int) -> None:
        self.ttl = timedelta(seconds=ttl_seconds)
        self.max_entries = max_entries
        self._entries: "OrderedDict[K, CacheEntry[V]]" = OrderedDict()

    def get(self, key: K) -> Optional[V]:
        entry = self._entries.get(key)
        if not entry:
            return None
        if utc_now() - entry.timestamp > self.ttl:
            self._entries.pop(key, None)
            return None
        self._entries.move_to_end(key)
        return entry.value

    def set(self, key: K, value: V) -> None:
        if key in self._entries:
            self._entries.move_to_end(key)
        self._entries[key] = CacheEntry(value=value, timestamp=utc_now())
        if len(self._entries) > self.max_entries:
            self._entries.popitem(last=False)
