from codings import best

def test_identity_and_tie():
    assert best("br;q=0.1, gzip;q=0.8") == "gzip"
    assert best("gzip;q=0.5, deflate;q=0.5") == "gzip"
