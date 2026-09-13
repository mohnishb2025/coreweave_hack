from disp import filename

def test_star_wins_over_plain():
    header = 'attachment; filename="cafe.txt"; filename*=UTF-8\'\'caf%C3%A9.txt'
    assert filename(header) == "café.txt"
