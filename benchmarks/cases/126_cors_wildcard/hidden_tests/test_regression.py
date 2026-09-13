from cors import allows

def test_apex_and_reject():
    assert allows("https://ex.com", ["https://*.ex.com"]) is True
    assert allows("https://evil.com", ["https://*.ex.com"]) is False
