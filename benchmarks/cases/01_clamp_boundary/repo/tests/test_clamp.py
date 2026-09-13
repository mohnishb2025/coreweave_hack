from clamp import clamp

def test_upper_boundary_is_inclusive():
    assert clamp(10, 0, 10) == 10
