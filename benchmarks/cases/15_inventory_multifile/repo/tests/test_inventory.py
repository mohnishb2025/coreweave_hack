from inventory import reserve

def test_before_snapshot_is_unchanged():
    before, after = reserve({"widget": 5}, "widget", 2)
    assert before == {"widget": 5}
    assert after == {"widget": 3}
