from links import href_for

def test_prev_is_the_second_link():
    assert href_for('<https://a>; rel="next", <https://b>; rel="prev"', "prev") == "https://b"
