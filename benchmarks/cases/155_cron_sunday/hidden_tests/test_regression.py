from crons import sunday

def test_name_and_monday():
    assert sunday("sun") is True
    assert sunday("1") is False
