from csp import allows

def test_evil_is_not_listed():
    assert allows("default-src 'self'; script-src https://cdn.ex.com", "https://evil.com") is False
