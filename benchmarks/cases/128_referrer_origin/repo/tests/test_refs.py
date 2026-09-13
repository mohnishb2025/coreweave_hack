from refs import origin_of

def test_default_https_port_is_dropped():
    assert origin_of("https://ex.com:443/path?q=1") == "https://ex.com"
