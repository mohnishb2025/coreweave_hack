from parts import part_name

def test_unquoted_and_filename_neighbor():
    assert part_name("form-data; name=hello") == "hello"
    assert part_name('form-data; name="z"; filename="a.txt"') == "z"
