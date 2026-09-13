from blanks import words

def test_repeat_spaces_and_tabs():
    assert words("a  b") == ["a", "b"]
    assert words("a\tb") == ["a", "b"]
