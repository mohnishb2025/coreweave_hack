from leap import is_leap

def test_400_year_rule_and_ordinary_leaps():
    assert is_leap(2000) is True
    assert is_leap(2004) is True
    assert is_leap(2100) is False
    assert is_leap(2019) is False
