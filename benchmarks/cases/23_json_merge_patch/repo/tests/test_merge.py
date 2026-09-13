from merge import merge_patch

def test_null_deletes_the_key():
    assert merge_patch({"a": 1, "b": 2}, {"a": None}) == {"b": 2}
