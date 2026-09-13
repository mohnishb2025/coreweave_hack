from slices import slice_start

def test_prefix_open_end_and_other_suffix():
    assert slice_start(1000, "bytes=0-499") == 0
    assert slice_start(1000, "bytes=500-") == 500
    assert slice_start(1000, "bytes=-50") == 950
