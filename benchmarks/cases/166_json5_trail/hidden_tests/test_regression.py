from json5s import load

def test_object_comma_and_plain():
    assert load('{"a": 1,}') == {"a": 1}
    assert load("[3]") == [3]
