from cssurls import url_of

def test_quoted_url():
    assert url_of('url("foo.png")') == "foo.png"
