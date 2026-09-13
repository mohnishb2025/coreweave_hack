from waits import millis

def test_fractional_seconds():
    assert millis("1.5s") == 1500
