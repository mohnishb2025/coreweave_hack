from clamps import clamp

def test_preferred_inside_range():
    assert clamp("clamp(10px, 20px, 30px)") == 20
