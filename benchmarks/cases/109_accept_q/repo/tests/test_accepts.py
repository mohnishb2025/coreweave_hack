from accepts import best

def test_default_q_beats_low_q():
    assert best("text/plain;q=0.1, text/html") == "text/html"
