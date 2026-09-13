from versions import same

def test_extra_zeros_and_numeric():
    assert same("1.2.0", "1.2.0.0") is True
    assert same("1.10", "1.9") is False
