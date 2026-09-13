from datetime import datetime
from stamps import parse

def test_other_zulu_and_offsets():
    assert parse("2024-12-31T23:59:59Z") == datetime.fromisoformat("2024-12-31T23:59:59+00:00")
    assert parse("2020-06-01T12:00:00-05:00") == datetime.fromisoformat("2020-06-01T12:00:00-05:00")
