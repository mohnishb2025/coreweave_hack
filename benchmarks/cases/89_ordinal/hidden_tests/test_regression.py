from ranks import ordinal

def test_teen_and_twenty_first():
    assert ordinal(2) == "2nd"
    assert ordinal(3) == "3rd"
    assert ordinal(11) == "11th"
    assert ordinal(21) == "21st"
    assert ordinal(22) == "22nd"
