from intervals import merge

def test_overlapping_out_of_order_ranges_collapse():
    assert merge([[8, 10], [1, 3], [2, 6]]) == [[1, 6], [8, 10]]
