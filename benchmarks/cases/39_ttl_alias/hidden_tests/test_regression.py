from ttl import get

def test_copy_and_strict_expiry():
    cache = {"session": {"value": ["ok"], "expires": 10}}
    got = get(cache, "session", 9)
    assert got == ["ok"]
    got.append("mutated")
    assert get(cache, "session", 9) == ["ok"]
    assert get(cache, "session", 11) is None
    assert get(cache, "missing", 1) is None
