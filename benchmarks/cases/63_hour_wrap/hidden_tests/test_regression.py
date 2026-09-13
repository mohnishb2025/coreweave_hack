from clocks import wrap_hour

def test_other_multi_day_wraps():
    assert wrap_hour(-1) == 23
    assert wrap_hour(49) == 1
    assert wrap_hour(48) == 0
