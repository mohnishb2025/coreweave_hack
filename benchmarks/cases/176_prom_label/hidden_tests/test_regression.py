from series import labels

def test_two_labels_and_bare_name():
    assert labels('up{job="api",code="200"}') == {"job": "api", "code": "200"}
    assert labels("up") == {}
