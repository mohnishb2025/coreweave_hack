from conds import modified_since

def test_equal_is_not_modified():
    assert modified_since(100, 100) is False
