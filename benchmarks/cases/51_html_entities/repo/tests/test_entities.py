from entities import unescape

def test_lt_entity_becomes_a_bracket():
    assert unescape("a&lt;b") == "a<b"
