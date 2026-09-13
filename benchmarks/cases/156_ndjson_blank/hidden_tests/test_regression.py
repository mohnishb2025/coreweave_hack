from ndjson import load

def test_spaces_and_single():
    assert load('{"a": 1}\n  \n{"c": 3}') == [{"a": 1}, {"c": 3}]
    assert load('{"z": 9}') == [{"z": 9}]
