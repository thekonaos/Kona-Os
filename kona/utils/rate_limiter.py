from __future__ import annotations
import time


class RateLimiter:
    def __init__(self, calls: int = 10, period: float = 60.0) -> None:
        self._calls = calls
        self._period = period
        self._timestamps: list[float] = []

    def is_allowed(self) -> bool:
        now = time.time()
        self._timestamps = [t for t in self._timestamps if now - t < self._period]
        if len(self._timestamps) < self._calls:
            self._timestamps.append(now)
            return True
        return False
