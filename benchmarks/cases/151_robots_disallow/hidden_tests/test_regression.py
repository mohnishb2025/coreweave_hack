from robots import allowed

def test_prefix_and_public():
    text = "User-agent: *\nDisallow: /admin\n"
    assert allowed(text, "/admin/users") is False
    assert allowed(text, "/public") is True
