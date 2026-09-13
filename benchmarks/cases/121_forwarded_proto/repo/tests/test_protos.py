from protos import proto

def test_leftmost_original_proto():
    assert proto("for=1.1.1.1;proto=https, for=2.2.2.2;proto=http") == "https"
