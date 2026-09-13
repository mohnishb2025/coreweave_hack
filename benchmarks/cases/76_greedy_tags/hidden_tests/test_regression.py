from markup import text_of

def test_adjacent_tags_and_trailing_text():
    assert text_of("<b>a</b><i>b</i>") == "ab"
    assert text_of("pre<b>x</b>post") == "prexpost"
