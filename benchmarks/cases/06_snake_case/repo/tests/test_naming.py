from naming import snake_case

def test_acronym_is_one_word():
    assert snake_case("HTTPServer") == "http_server"
