from ids import canonical

def test_compact_hex_gets_hyphens():
    assert canonical("550e8400E29B41D4A716446655440000") == "550e8400-e29b-41d4-a716-446655440000"
