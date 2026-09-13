from stats import median

def test_odd_length_and_unsorted_input():
    assert median([3, 1, 2]) == 2
    assert median([9]) == 9
    assert median([8, 2]) == 5
