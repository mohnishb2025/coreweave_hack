from .accounts import copy_accounts

def transfer(accounts, source, dest, amount):
    working = copy_accounts(accounts)
    working[source] -= amount
    if working[source] < 0:
        raise ValueError("insufficient funds")
    working[dest] += amount
    return working
