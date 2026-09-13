from wraps import wrap

def test_packs_short_words():
    assert wrap("foo bar baz", 7) == ["foo bar", "baz"]
    assert wrap("aa bb cc", 5) == ["aa bb", "cc"]
