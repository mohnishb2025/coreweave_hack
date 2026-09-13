from origins import host

def test_userinfo_is_not_the_host():
    assert host("https://user@ex.com/a") == "ex.com"
