from duration import seconds

def test_day_and_hour_components():
    assert seconds("P1DT2H") == 93600
