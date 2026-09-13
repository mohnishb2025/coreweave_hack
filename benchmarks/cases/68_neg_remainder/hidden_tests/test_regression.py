from remainders import remainder

def test_other_signs_match_python_mod():
    assert remainder(-7, 3) == 2
    assert remainder(7, 3) == 1
    assert remainder(-4, 2) == 0
