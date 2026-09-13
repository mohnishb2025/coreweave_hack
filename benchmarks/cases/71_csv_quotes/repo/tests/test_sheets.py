from sheets import split_row

def test_quoted_comma_is_one_field():
    assert split_row('a,"b,c",d') == ["a", "b,c", "d"]
