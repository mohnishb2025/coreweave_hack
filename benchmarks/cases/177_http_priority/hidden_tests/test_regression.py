from prios import urgency

def test_urgency_second_and_default():
    assert urgency("i, u=1") == 1
    assert urgency("") == 3
