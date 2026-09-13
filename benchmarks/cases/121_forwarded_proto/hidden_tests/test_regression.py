from protos import proto

def test_only_proto_and_spaces():
    assert proto("proto=http") == "http"
    assert proto(" for=10.0.0.1;proto=https ") == "https"
