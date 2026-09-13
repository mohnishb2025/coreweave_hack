from money import quantize

def test_halfway_value_ties_to_even():
    assert quantize("1.225") == "1.22"
