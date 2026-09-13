from overlap import overlaps

def test_touching_endpoints_overlap():
    assert overlaps([1, 2], [2, 3]) is True
