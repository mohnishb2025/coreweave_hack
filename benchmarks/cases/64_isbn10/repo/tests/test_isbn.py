from isbn import valid

def test_plain_isbn10():
    assert valid("0306406152") is True
