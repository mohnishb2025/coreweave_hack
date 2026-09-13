from store import cached_profile

def test_falsey_profile_is_cached():
    calls = []
    loader = lambda key: calls.append(key) or {}
    cached_profile("u", loader)
    cached_profile("u", loader)
    assert calls == ["u"]
