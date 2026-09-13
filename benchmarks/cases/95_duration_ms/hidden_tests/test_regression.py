from waits import millis

def test_ms_and_whole_seconds():
    assert millis("200ms") == 200
    assert millis("2s") == 2000
