from payload import parse_json

def test_plain_object_and_array():
    assert parse_json('{"b": 2}') == {"b": 2}
    assert parse_json("[1, 2]") == [1, 2]
    assert parse_json("\ufeff[3]") == [3]
