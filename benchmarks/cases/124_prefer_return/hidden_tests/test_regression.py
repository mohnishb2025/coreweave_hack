from prefers import return_to

def test_return_is_not_first():
    assert return_to("wait=5, return=representation") == "representation"
    assert return_to("return=minimal") == "minimal"
