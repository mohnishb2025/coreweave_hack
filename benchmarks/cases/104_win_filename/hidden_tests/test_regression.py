from filesafe import safe

def test_colon_trailing_dot_and_con():
    assert safe("foo:bar") == "foo_bar"
    assert safe("file.") == "file"
    assert safe("CON") == "_CON"
