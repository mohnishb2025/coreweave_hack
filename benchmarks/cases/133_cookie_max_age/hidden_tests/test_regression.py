from ages import max_age

def test_order_and_zero():
    assert max_age("Max-Age=0; id=1") == 0
    assert max_age("id=1; max-age=5") == 5
