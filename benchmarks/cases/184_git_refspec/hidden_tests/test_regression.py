from refspecs import source

def test_wildcard_and_other_force():
    assert source("refs/heads/*:refs/remotes/origin/*") == "refs/heads/*"
    assert source("+refs/heads/dev:refs/heads/dev") == "refs/heads/dev"
