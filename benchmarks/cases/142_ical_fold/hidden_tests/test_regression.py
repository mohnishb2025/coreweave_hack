from vevents import unfold

def test_lf_fold_and_plain():
    assert unfold("SUMMARY:Hel\n lo") == "SUMMARY:Hello"
    assert unfold("UID:abc") == "UID:abc"
