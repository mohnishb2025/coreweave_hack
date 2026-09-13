from isbn13 import valid

def test_plain_isbn13():
    assert valid("9780306406157") is True
