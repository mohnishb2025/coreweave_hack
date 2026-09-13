from delays import seconds

def test_seconds_and_hours():
    assert seconds("90s") == 90
    assert seconds("1h") == 3600
