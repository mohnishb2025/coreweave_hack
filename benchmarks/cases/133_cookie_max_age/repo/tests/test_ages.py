from ages import max_age

def test_max_age_attribute():
    assert max_age("id=1; Max-Age=60") == 60
