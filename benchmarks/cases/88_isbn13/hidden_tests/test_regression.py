from isbn13 import valid

def test_hyphens_and_reject():
    assert valid("978-0-306-40615-7") is True
    assert valid("9780306406158") is False
