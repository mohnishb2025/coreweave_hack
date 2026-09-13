from slices import slice_start

def test_last_two_hundred_bytes():
    assert slice_start(1000, "bytes=-200") == 800
