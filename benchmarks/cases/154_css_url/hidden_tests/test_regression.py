from cssurls import url_of

def test_single_and_bare():
    assert url_of("url('bar.png')") == "bar.png"
    assert url_of("url(baz.png)") == "baz.png"
