import time
import pytest
from kona.utils.cache import TTLCache
from kona.utils.rate_limiter import RateLimiter
from kona.utils.logger import get_logger
from kona import __version__


def test_cache_set_get():
    c = TTLCache(ttl=60.0)
    c.set("k", "v")
    assert c.get("k") == "v"


def test_cache_miss():
    c = TTLCache()
    assert c.get("nope") is None


def test_cache_ttl_expiry():
    c = TTLCache(ttl=0.01)
    c.set("x", 42)
    time.sleep(0.05)
    assert c.get("x") is None


def test_cache_clear():
    c = TTLCache()
    c.set("a", 1)
    c.clear()
    assert c.get("a") is None


def test_cache_overwrite():
    c = TTLCache()
    c.set("k", "first")
    c.set("k", "second")
    assert c.get("k") == "second"


def test_rate_limiter_allows():
    r = RateLimiter(calls=5, period=60.0)
    results = [r.is_allowed() for _ in range(5)]
    assert all(results)


def test_rate_limiter_blocks():
    r = RateLimiter(calls=3, period=60.0)
    for _ in range(3):
        r.is_allowed()
    assert not r.is_allowed()


def test_rate_limiter_single():
    r = RateLimiter(calls=1, period=60.0)
    assert r.is_allowed()
    assert not r.is_allowed()


def test_logger_name():
    logger = get_logger("kernel")
    assert logger.name == "kernel"


def test_logger_different_names():
    a = get_logger("a")
    b = get_logger("b")
    assert a.name != b.name


def test_version():
    assert __version__ == "0.1.0"
