from vevents import unfold

def test_folded_description():
    assert unfold("DESCRIPTION:Hello\r\n World") == "DESCRIPTION:HelloWorld"
