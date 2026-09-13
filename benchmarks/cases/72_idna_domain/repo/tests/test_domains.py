from domains import ascii_host

def test_umlaut_domain_becomes_punycode():
    assert ascii_host("Bücher.de") == "xn--bcher-kva.de"
