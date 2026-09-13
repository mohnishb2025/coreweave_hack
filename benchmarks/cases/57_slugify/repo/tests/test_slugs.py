from slugs import slug

def test_punctuation_is_not_kept():
    assert slug("Hello, World!") == "hello-world"
