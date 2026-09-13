from cachectl import max_age

def test_case_and_order():
    assert max_age("Max-Age=0, no-store") == 0
    assert max_age("max-age=3600, public") == 3600
