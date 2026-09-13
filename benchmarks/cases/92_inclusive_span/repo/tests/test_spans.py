from spans import values

def test_includes_the_end():
    assert values(1, 3) == [1, 2, 3]
