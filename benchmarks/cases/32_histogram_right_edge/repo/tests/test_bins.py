from bins import bin_index

def test_rightmost_edge_belongs_to_last_bin():
    assert bin_index([0, 10, 20], 20) == 1
