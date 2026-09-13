from luhn import valid

def test_doubled_digits_and_rejects():
    assert valid("4111111111111111") is True
    assert valid("1234567890123452") is True
    assert valid("4111111111111112") is False
