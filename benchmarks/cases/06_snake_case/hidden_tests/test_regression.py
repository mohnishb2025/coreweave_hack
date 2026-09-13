from naming import snake_case

def test_identifier_with_acronym():
    assert snake_case("parseJSONValue") == "parse_json_value"
