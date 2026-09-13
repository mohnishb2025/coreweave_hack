from masks import mask

def test_digits_only_and_dashes():
    assert mask("4111111111111111") == "************1111"
    assert mask("4111-1111-1111-1111") == "************1111"
