from leap import is_leap

def test_century_not_divisible_by_400_is_common():
    assert is_leap(1900) is False
