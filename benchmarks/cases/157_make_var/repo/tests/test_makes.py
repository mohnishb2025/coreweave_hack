from makes import value

def test_spaces_around_equals():
    assert value("FOO = bar\n", "FOO") == "bar"
