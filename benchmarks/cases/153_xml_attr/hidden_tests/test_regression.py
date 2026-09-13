from attrs import attr

def test_src_and_later_alt():
    assert attr('<img src="x.jpg" alt="a b">', "alt") == "a b"
    assert attr('<a href="z">', "href") == "z"
