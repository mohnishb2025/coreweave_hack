from media import type_of

def test_json_and_spaces():
    assert type_of("application/JSON; charset=utf-8") == "application/json"
    assert type_of(" text/plain ") == "text/plain"
