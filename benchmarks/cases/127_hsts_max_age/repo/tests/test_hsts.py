from hsts import max_age

def test_year_and_subdomains():
    assert max_age("max-age=31536000; includeSubDomains") == 31536000
