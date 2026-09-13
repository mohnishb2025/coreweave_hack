from masks import mask

def test_spaces_are_not_counted():
    assert mask("4111 1111 1111 1111") == "************1111"
