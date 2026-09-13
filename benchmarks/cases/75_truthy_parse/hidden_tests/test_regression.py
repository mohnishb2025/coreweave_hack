from flags import is_true

def test_zero_yes_and_true():
    assert is_true("0") is False
    assert is_true("yes") is True
    assert is_true("TRUE") is True
