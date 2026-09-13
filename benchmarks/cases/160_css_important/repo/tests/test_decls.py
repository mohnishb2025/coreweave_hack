from decls import decl

def test_important_is_not_the_value():
    assert decl("color: red !important") == "red"
