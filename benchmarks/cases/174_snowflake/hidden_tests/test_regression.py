from flakes import timestamp_ms

def test_later_id_keeps_worker_bits():
    assert timestamp_ms(20971520042) == 1288834979657
