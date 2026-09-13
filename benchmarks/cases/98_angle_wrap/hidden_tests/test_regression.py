from angles import wrap

def test_negative_and_single_turn():
    assert wrap(-370) == 350
    assert wrap(370) == 10
