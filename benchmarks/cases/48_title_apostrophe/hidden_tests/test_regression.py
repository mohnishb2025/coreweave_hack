from titles import title_case

def test_other_contractions_and_spaces():
    assert title_case("o'clock") == "O'clock"
    assert title_case("don't stop") == "Don't Stop"
    assert title_case("abc def") == "Abc Def"
