from flags import is_true

def test_false_string_is_false():
    assert is_true("false") is False
