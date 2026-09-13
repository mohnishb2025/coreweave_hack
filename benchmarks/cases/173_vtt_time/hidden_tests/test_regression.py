from vtts import millis

def test_hour_and_short_form():
    assert millis("01:00:00.000") == 3600000
    assert millis("00:01.500") == 1500
