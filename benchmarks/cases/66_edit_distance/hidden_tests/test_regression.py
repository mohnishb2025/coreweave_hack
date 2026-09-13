from distance import distance

def test_substitution_and_saturday():
    assert distance("kitten", "sitten") == 1
    assert distance("Saturday", "Sunday") == 3
