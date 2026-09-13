from refspecs import source

def test_forced_main():
    assert source("+refs/heads/main:refs/remotes/origin/main") == "refs/heads/main"
