from transposes import distance

def test_adjacent_swap_is_one():
    assert distance("ab", "ba") == 1
