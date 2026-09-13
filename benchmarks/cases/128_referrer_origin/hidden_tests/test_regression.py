from refs import origin_of

def test_custom_port_and_http():
    assert origin_of("http://ex.com:8080/a") == "http://ex.com:8080"
    assert origin_of("http://ex.com:80/x") == "http://ex.com"
