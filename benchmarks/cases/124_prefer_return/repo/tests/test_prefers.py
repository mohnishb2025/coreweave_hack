from prefers import return_to

def test_minimal_preference():
    assert return_to("return=minimal, wait=10") == "minimal"
