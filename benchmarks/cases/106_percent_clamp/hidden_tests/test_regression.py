from percents import clamp

def test_negative_and_interior():
    assert clamp(-3) == 0
    assert clamp(40) == 40
