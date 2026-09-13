from sfvs import is_true

def test_true_token_and_plain_zero():
    assert is_true("?1") is True
    assert is_true("0") is False
