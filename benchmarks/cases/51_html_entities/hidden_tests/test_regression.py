from entities import unescape

def test_quotes_and_double_encoded_amp():
    assert unescape("&quot;x&quot;") == '"x"'
    assert unescape("&amp;lt;") == "&lt;"
    assert unescape("ok") == "ok"
