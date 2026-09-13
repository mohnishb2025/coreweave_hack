from ids import canonical

def test_braces_and_urn():
    assert canonical("{550e8400-e29b-41d4-a716-446655440000}") == "550e8400-e29b-41d4-a716-446655440000"
    assert canonical("urn:uuid:550e8400-e29b-41d4-a716-446655440000") == "550e8400-e29b-41d4-a716-446655440000"
