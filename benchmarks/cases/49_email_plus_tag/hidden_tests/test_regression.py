from email import canonical

def test_domain_case_and_missing_tag():
    assert canonical("root@EXAMPLE.COM") == "root@example.com"
    assert canonical("Ada+one+two@Example.com") == "ada@example.com"
    assert canonical("no-tag@Example.com") == "no-tag@example.com"
