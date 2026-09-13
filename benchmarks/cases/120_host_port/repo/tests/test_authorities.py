from authorities import hostname

def test_port_is_not_the_host():
    assert hostname("ex.com:8080") == "ex.com"
