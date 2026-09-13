from wkts import coords

def test_simple_point():
    assert coords("POINT(1 2)") == (1.0, 2.0)
