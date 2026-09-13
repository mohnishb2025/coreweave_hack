from inventory import reserve

def test_snapshots_are_distinct_objects():
    before, after = reserve({"x": 2}, "x", 1)
    assert before is not after
