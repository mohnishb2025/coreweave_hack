from angles import turns

def test_grad_and_turn_units():
    assert turns("200grad") == 0.5
    assert turns("0.5turn") == 0.5
