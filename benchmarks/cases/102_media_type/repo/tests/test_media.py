from media import type_of

def test_charset_is_not_kept():
    assert type_of("Text/HTML; charset=UTF-8") == "text/html"
