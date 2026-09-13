from store import cached_profile

def test_none_value_is_cached():
    calls = []
    loader = lambda key: calls.append(key)
    cached_profile("none", loader)
    cached_profile("none", loader)
    assert calls == ["none"]
