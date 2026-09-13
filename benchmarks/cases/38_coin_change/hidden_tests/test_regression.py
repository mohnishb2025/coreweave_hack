from change import min_coins

def test_other_canonical_and_impossible_amounts():
    assert min_coins(24, [1, 5, 12, 21]) == 2
    assert min_coins(30, [1, 5, 12, 21]) == 4
    assert min_coins(0, [1, 5]) == 0
    assert min_coins(3, [2, 4]) == -1
