from crons import sunday

def test_seven_is_sunday():
    assert sunday("7") is True
