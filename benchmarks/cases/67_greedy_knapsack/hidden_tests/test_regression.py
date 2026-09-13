from packs import max_value

def test_ratio_order_is_not_enough():
    assert max_value([(2, 3), (3, 4), (4, 5)], 6) == 8
    assert max_value([(1, 1)], 0) == 0
