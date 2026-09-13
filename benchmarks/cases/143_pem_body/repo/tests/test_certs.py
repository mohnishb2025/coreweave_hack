from certs import body

def test_hello_der():
    pem = "-----BEGIN CERT-----\naGk=\n-----END CERT-----\n"
    assert body(pem) == b"hi"
