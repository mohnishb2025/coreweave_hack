from decls import decl

def test_colon_in_value_and_other_important():
    assert decl('content: "a:b"') == '"a:b"'
    assert decl("margin: 0 !important") == "0"
