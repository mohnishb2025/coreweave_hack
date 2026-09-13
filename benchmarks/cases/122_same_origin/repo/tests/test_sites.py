from sites import same

def test_default_https_port():
    assert same("https://ex.com", "https://ex.com:443") is True
