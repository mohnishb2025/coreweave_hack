from authorities import hostname

def test_ipv6_and_plain():
    assert hostname("[::1]:80") == "::1"
    assert hostname("ex.com") == "ex.com"
