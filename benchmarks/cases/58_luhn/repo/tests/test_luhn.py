from luhn import valid

def test_classic_account_number():
    assert valid("79927398713") is True
