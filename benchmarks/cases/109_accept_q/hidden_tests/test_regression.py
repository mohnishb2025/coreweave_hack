from accepts import best

def test_explicit_q_and_first_on_ties():
    assert best("text/plain;q=0.2, application/json;q=0.8") == "application/json"
    assert best("a;q=0.5, b;q=0.5") == "a"
