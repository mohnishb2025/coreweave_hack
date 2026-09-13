from afters import delay

def test_http_date_delay():
    assert delay("Wed, 21 Oct 2015 07:28:00 GMT", 1445412420) == 60
