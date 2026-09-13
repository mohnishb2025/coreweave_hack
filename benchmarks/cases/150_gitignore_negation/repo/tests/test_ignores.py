from ignores import ignored

def test_negation_restores_file():
    assert ignored("keep.log", ["*.log", "!keep.log"]) is False
