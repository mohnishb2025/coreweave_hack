from links import href_for

def test_next_and_unquoted_rel():
    assert href_for('<https://a>; rel="next", <https://b>; rel="prev"', "next") == "https://a"
    assert href_for('<https://a>; rel="next", <https://c>; rel=last', "last") == "https://c"
