from ignores import ignored

def test_broader_negation_and_drop():
    assert ignored("keep.log", ["*.log", "!keep.*"]) is False
    assert ignored("drop.log", ["*.log", "!keep.log"]) is True
