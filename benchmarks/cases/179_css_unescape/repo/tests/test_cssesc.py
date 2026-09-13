from cssesc import unescape

def test_hex_bang():
    assert unescape("hello\\21") == "hello!"
