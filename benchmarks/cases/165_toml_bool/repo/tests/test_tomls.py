from tomls import value

def test_true_is_boolean():
    assert value("enabled = true") is True
