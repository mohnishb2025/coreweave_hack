from cors import allows

def test_subdomain_wildcard():
    assert allows("https://app.ex.com", ["https://*.ex.com"]) is True
