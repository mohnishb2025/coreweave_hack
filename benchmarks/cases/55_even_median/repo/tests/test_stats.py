from stats import median

def test_even_length_averages_the_middle_pair():
    assert median([1, 2, 3, 4]) == 2.5
