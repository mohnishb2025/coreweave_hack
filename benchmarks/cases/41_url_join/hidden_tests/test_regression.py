from urls import join

def test_absolute_relative_and_rooted_paths():
    assert join("http://ex.com/dir/page", "/rooted") == "http://ex.com/rooted"
    assert join("http://ex.com/dir/page", "https://other.test/x") == "https://other.test/x"
    assert join("http://ex.com/dir/", "next") == "http://ex.com/dir/next"
