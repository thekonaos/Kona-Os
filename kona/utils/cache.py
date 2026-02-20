from __future__ import annotations
import time
from typing import Any


class TTLCache:
    def __init__(self, ttl: float = 300.0) -> None:
        self._ttl = ttl
        self._store: dict[str, tuple[Any, float]] = {}

    def get(self, key: str) -> Any | None:
        entry = self._store.get(key)
        if entry and time.time() - entry[1] < self._ttl:
            return entry[0]
        return None

    def set(self, key: str, value: Any) -> None:
        self._store[key] = (value, time.time())

    def clear(self) -> None:
        self._store.clear()
