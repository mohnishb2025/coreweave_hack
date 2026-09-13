from origins import host

def test_port_and_plain():
    assert host("https://ex.com:8080/a") == "ex.com"
    assert host("http://ex.com") == "ex.com"
