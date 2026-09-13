from ttl import get

def test_value_is_fresh_on_the_expiry_instant():
    cache = {"session": {"value": ["ok"], "expires": 10}}
    assert get(cache, "session", 10) == ["ok"]
