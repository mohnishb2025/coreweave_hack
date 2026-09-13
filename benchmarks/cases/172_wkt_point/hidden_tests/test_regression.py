from wkts import coords

def test_space_after_type_and_case():
    assert coords("POINT (3 4)") == (3.0, 4.0)
    assert coords("point(5 6)") == (5.0, 6.0)
