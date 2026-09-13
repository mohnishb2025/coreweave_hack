from flakes import timestamp_ms

def test_twitter_epoch_offset():
    assert timestamp_ms(4194304000) == 1288834975657
