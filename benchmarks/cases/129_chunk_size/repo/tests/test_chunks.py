from chunks import size

def test_hex_chunk_size():
    assert size("1a") == 26
