from datetime import timezone
from timestamps import parse_timestamp

def test_utc_z_suffix():
    assert parse_timestamp("2025-01-02T03:04:05Z").tzinfo == timezone.utc
