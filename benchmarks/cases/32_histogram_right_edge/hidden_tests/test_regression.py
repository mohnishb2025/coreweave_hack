import pytest
from bins import bin_index

def test_interior_edges_and_out_of_range():
    assert bin_index([0, 10, 20], 0) == 0
    assert bin_index([0, 10, 20], 10) == 1
    assert bin_index([0, 10, 20], 19.9) == 1
    assert bin_index([0, 5, 10], 10) == 1
    with pytest.raises(ValueError):
        bin_index([0, 10, 20], -0.1)
    with pytest.raises(ValueError):
        bin_index([0, 10, 20], 20.1)
