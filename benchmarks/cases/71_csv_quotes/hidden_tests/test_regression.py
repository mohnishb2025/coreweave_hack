from sheets import split_row

def test_escaped_quotes_and_empty_fields():
    assert split_row('a,"b""c",d') == ["a", 'b"c', "d"]
    assert split_row("a,,c") == ["a", "", "c"]
