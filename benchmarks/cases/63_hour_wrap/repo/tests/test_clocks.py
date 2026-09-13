from clocks import wrap_hour

def test_minus_twenty_five_is_23():
    assert wrap_hour(-25) == 23
