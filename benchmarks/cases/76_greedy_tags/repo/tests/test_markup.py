from markup import text_of

def test_simple_bold():
    assert text_of("<b>hi</b>") == "hi"
