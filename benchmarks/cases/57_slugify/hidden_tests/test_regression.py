from slugs import slug

def test_repeats_underscores_and_edges():
    assert slug("Hello   World") == "hello-world"
    assert slug("already_slug") == "already-slug"
    assert slug("--Hello--") == "hello"
