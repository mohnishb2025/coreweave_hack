from cachectl import max_age

def test_public_max_age():
    assert max_age("public, max-age=60") == 60
