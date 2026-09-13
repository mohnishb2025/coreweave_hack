from chunks import chunks

def test_final_partial_chunk():
    assert chunks([1, 2, 3], 2) == [[1, 2], [3]]
