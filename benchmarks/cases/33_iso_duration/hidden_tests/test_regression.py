from duration import seconds

def test_weeks_minutes_and_seconds():
    assert seconds("P1W") == 604800
    assert seconds("PT1H2M3S") == 3723
    assert seconds("PT90S") == 90
    assert seconds("P1DT0H") == 86400
