from parts import part_name

def test_quoted_name():
    assert part_name('form-data; name="q"') == "q"
