from .model import snapshot

def reserve(stock, sku, amount):
    before = snapshot(stock)
    stock[sku] -= amount
    return before, stock
