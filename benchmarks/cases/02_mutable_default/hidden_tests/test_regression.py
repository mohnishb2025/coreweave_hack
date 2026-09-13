from collector import collect

def test_three_fresh_calls():
    assert [collect(i) for i in range(3)] == [[0], [1], [2]]
