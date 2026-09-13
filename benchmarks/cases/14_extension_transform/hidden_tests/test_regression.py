from paths import replace_extension

def test_hidden_file():
    assert replace_extension(".env", "example") == ".env.example"
