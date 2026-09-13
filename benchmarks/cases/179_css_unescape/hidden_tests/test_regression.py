from cssesc import unescape

def test_newline_and_plain():
    assert unescape("x\\A") == "x\n"
    assert unescape("ok") == "ok"
