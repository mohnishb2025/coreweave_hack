from urls import join

def test_parent_segment_walks_up_the_base_path():
    assert join("http://ex.com/dir/page", "../other") == "http://ex.com/other"
