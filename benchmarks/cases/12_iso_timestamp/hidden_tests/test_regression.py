from timestamps import parse_timestamp

def test_offset_suffix():
    assert parse_timestamp("2025-01-02T03:04:05+02:00").utcoffset().total_seconds() == 7200
