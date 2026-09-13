from cpaths import cookie_path

def test_lowercase_and_default():
    assert cookie_path("a=b; path=/api; Secure") == "/api"
    assert cookie_path("a=b") == "/"
