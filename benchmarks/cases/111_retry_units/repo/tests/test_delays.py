from delays import seconds

def test_minutes():
    assert seconds("2m") == 120
