from titles import title_case

def test_apostrophe_does_not_start_a_new_word():
    assert title_case("it's fine") == "It's Fine"
