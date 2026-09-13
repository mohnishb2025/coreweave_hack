from ulids import millis

def test_other_timestamp():
    assert millis("01BX5ZZKBKABCDEABCDEABCDE0") == 1508808576371
