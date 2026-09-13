from distance import distance

def test_mid_string_delete_is_one_edit():
    assert distance("abc", "ac") == 1
