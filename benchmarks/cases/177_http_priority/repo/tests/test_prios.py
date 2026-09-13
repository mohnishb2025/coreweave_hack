from prios import urgency

def test_incremental_with_urgency():
    assert urgency("u=3, i") == 3
