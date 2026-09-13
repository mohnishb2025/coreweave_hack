from payloads import decode

def test_raw_and_other_base64():
    assert decode("data:,hello") == "hello"
    assert decode("data:text/plain;base64,Ynk=") == "by"
