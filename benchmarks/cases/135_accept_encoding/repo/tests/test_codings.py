from codings import best

def test_default_q_beats_deflate():
    assert best("deflate;q=0.5, gzip") == "gzip"
