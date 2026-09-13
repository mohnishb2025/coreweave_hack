from exports import value

def test_export_and_escaped_quote():
    assert value("export NAME=x") == "x"
    assert value('NAME="a\"b"') == 'a"b'
