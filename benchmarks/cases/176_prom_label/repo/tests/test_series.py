from series import labels

def test_one_label():
    assert labels('up{job="api"}') == {"job": "api"}
