from chunks import chunks

def test_exact_chunk_is_retained():
    assert chunks([1, 2], 2) == [[1, 2]]
