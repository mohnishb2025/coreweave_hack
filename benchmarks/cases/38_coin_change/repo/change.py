def min_coins(amount, coins):
    coins = sorted(coins, reverse=True)
    used = 0
    for coin in coins:
        used += amount // coin
        amount %= coin
    return used if amount == 0 else -1
