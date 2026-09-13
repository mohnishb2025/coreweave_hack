from images import split_ref

def test_explicit_tag():
    assert split_ref("nginx:1.25") == ("nginx", "1.25")
