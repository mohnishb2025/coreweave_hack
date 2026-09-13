from transposes import distance

def test_swap_and_ordinary_edits():
    assert distance("ca", "ac") == 1
    assert distance("kitten", "sitten") == 1
