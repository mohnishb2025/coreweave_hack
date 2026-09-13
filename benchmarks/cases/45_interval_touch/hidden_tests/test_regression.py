from overlap import overlaps

def test_containment_and_disjoint():
    assert overlaps([1, 5], [2, 3]) is True
    assert overlaps([2, 3], [1, 5]) is True
    assert overlaps([1, 2], [3, 4]) is False
    assert overlaps([5, 5], [5, 5]) is True
