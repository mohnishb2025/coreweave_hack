from csp import allows

def test_cdn_and_lookalike():
    header = "default-src 'self'; script-src https://cdn.ex.com"
    assert allows(header, "https://cdn.ex.com") is True
    assert allows(header, "https://cdn.ex.com.evil") is False
