from disp import filename

def test_star_only_and_space():
    assert filename("attachment; filename*=UTF-8''hi%20there.txt") == "hi there.txt"
    assert filename('inline; filename="plain.txt"') == "plain.txt"
