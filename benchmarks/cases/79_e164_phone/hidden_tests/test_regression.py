from phones import e164

def test_spaces_and_00_prefix():
    assert e164("+1 202 555 0100") == "+12025550100"
    assert e164("0012025550100") == "+12025550100"
