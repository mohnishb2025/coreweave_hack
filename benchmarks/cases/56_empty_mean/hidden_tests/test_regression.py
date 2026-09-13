from average import mean

def test_ordinary_averages_are_true_division():
    assert mean([1, 2]) == 1.5
    assert mean([2, 4]) == 3
