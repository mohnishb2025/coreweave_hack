from ibans import valid

def test_spaced_uk_and_reject():
    assert valid("GB82 WEST 1234 5698 7654 32") is True
    assert valid("GB82WEST12345698765432") is True
    assert valid("GB82WEST12345698765433") is False
