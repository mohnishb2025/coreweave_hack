from rrules import days

def test_byday_before_freq():
    assert days("BYDAY=MO,WE;FREQ=WEEKLY") == ["MO", "WE"]
