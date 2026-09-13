from makes import value

def test_tight_and_later_spaced():
    assert value("FOO=bar\nBAZ=qux\n", "BAZ") == "qux"
    assert value("FOO = x\nBAR = y\n", "BAR") == "y"
