from robots import allowed

def test_admin_is_blocked():
    text = "User-agent: *\nDisallow: /admin\n"
    assert allowed(text, "/admin") is False
