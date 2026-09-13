from varies import fields

def test_star_and_spaces():
    assert fields("*") == ["*"]
    assert fields(" Origin , Accept ") == ["origin", "accept"]
