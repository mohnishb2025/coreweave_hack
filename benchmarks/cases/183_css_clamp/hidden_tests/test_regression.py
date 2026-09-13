from clamps import clamp

def test_below_min_and_above_max():
    assert clamp("clamp(10px, 5px, 30px)") == 10
    assert clamp("clamp(10px, 50px, 30px)") == 30
