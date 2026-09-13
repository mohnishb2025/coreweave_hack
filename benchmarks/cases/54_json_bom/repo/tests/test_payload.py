from payload import parse_json

def test_utf8_bom_is_ignored():
    assert parse_json("\ufeff{\"a\": 1}") == {"a": 1}
