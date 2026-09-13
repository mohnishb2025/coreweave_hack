from labels import sort_names

def test_file2_comes_before_file10():
    assert sort_names(["file10.txt", "file2.txt"]) == ["file2.txt", "file10.txt"]
