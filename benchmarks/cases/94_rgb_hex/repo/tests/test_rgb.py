from rgb import to_rgb

def test_short_hex():
    assert to_rgb("#abc") == (170, 187, 204)
