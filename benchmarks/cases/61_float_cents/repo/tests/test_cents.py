from cents import to_cents

def test_one_fifteen_is_one_hundred_fifteen_cents():
    assert to_cents(1.15) == 115
