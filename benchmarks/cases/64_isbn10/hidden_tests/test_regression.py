from isbn import valid

def test_hyphens_x_and_reject():
    assert valid("0-306-40615-2") is True
    assert valid("043942089X") is True
    assert valid("0306406153") is False
