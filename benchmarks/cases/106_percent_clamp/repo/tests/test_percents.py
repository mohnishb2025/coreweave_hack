from percents import clamp

def test_over_one_hundred():
    assert clamp(150) == 100
