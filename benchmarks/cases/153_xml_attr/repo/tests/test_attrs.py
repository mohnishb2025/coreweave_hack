from attrs import attr

def test_title_with_spaces():
    assert attr('<a title="hello world">', "title") == "hello world"
