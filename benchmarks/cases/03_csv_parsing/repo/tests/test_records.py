from records import parse_row

def test_quoted_comma():
    assert parse_row('"Doe, Jane","Austin"') == {"name": "Doe, Jane", "city": "Austin"}
