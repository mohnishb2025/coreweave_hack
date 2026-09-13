from ulids import millis

def test_crockford_timestamp():
    assert millis("01ARZ3NDEKTSV4RRFFQ69G5FAV") == 1469922850259
