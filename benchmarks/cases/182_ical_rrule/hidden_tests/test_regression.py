from rrules import days

def test_byday_last_and_other_days():
    assert days("FREQ=WEEKLY;BYDAY=TU,TH") == ["TU", "TH"]
    assert days("BYDAY=FR;FREQ=DAILY") == ["FR"]
