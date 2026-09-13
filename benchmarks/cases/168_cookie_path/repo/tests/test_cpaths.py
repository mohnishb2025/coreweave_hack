from cpaths import cookie_path

def test_admin_path():
    assert cookie_path("id=1; Path=/admin") == "/admin"
