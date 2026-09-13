from cents import to_cents

def test_binary_fractions_and_even_dollars():
    assert to_cents(19.99) == 1999
    assert to_cents(0.10) == 10
    assert to_cents(2.00) == 200
