from datetime import datetime
from stamps import parse

def test_zulu_is_utc():
    assert parse("2020-01-01T00:00:00Z") == datetime.fromisoformat("2020-01-01T00:00:00+00:00")
