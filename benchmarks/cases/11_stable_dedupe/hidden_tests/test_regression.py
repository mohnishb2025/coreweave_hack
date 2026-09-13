from dedupe import unique

def test_string_order():
    assert unique(["z", "a", "z", "m"]) == ["z", "a", "m"]
