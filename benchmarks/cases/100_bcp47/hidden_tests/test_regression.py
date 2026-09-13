from langs import canonical

def test_script_and_lowercase_region():
    assert canonical("ZH-hANS-cn") == "zh-Hans-CN"
    assert canonical("fr-fr") == "fr-FR"
