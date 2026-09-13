from hsts import max_age

def test_order_and_zero():
    assert max_age("includeSubDomains; max-age=0") == 0
    assert max_age("max-age=60") == 60
