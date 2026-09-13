from phones import e164

def test_parens_and_dashes():
    assert e164("+1 (202) 555-0100") == "+12025550100"
