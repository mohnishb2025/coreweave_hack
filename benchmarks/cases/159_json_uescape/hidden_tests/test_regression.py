from uescapes import unescape

def test_quote_and_plain():
    assert unescape("say \\u0022hi\\u0022") == 'say "hi"'
    assert unescape("ok") == "ok"
