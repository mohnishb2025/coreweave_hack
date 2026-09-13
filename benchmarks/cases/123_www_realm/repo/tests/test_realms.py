from realms import realm

def test_comma_inside_quoted_realm():
    assert realm('Basic realm="User, Admin", charset=UTF-8') == "User, Admin"
