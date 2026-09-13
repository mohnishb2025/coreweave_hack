from freshness import fresh

def test_equal_age_is_stale():
    assert fresh(60, 60) is False
