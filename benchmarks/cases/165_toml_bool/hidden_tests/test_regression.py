from tomls import value

def test_false_and_other_key():
    assert value("ok = false") is False
    assert value("ok = true") is True
