from conds import modified_since

def test_later_earlier_and_other_equal():
    assert modified_since(101, 100) is True
    assert modified_since(99, 100) is False
    assert modified_since(200, 200) is False
