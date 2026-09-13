from change import min_coins

def test_greedy_choice_is_not_always_optimal():
    assert min_coins(15, [1, 5, 12, 21]) == 3
