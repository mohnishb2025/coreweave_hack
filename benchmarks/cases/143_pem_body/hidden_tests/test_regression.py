from certs import body

def test_crlf_and_bye():
    pem = "-----BEGIN CERT-----\r\nYnk=\r\n-----END CERT-----\r\n"
    assert body(pem) == b"by"
