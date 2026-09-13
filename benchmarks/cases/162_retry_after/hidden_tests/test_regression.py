from afters import delay

def test_delta_seconds_and_other_date():
    assert delay("120", 0) == 120
    assert delay("Fri, 31 Dec 1999 23:59:59 GMT", 946684739) == 60
