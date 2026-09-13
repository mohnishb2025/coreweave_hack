from records import parse_row

def test_escaped_quote():
    assert parse_row('"A ""quoted"" name","Rome"')["name"] == 'A "quoted" name'
