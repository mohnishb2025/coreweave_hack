from sites import same

def test_http_port_and_mismatches():
    assert same("http://ex.com", "http://ex.com:80") is True
    assert same("https://ex.com", "http://ex.com") is False
    assert same("https://ex.com:8443", "https://ex.com") is False
