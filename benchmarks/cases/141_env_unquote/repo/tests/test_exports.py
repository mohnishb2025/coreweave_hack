from exports import value

def test_quoted_spaces():
    assert value('NAME="a b"') == "a b"
