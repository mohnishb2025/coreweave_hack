from packs import max_value

def test_two_fives_beat_one_six():
    assert max_value([(6, 6), (5, 5), (5, 5)], 10) == 10
