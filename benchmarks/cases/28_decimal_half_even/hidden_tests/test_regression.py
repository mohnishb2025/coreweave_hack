from money import quantize

def test_odd_tie_and_negative_half_even():
    assert quantize("1.235") == "1.24"
    assert quantize("-1.225") == "-1.22"
    assert quantize("1.220") == "1.22"
    assert quantize("1.215") == "1.22"
