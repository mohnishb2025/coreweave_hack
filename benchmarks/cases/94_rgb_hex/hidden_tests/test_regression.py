from rgb import to_rgb

def test_long_and_upper_short():
    assert to_rgb("#AABBCC") == (170, 187, 204)
    assert to_rgb("#fff") == (255, 255, 255)
