from payloads import decode

def test_base64_payload():
    assert decode("data:text/plain;base64,aGVsbG8=") == "hello"
