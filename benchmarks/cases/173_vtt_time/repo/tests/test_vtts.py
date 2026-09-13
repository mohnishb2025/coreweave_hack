from vtts import millis

def test_hour_minute_second():
    assert millis("00:01:02.000") == 62000
