from clamp import clamp

def test_values_above_upper_boundary():
    assert clamp(99, 0, 10) == 10
