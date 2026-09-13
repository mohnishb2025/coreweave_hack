from sfvs import is_true

def test_false_token():
    assert is_true("?0") is False
