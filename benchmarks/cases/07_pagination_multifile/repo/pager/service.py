from .math import divide_round_up

def page_count(items, page_size):
    return divide_round_up(len(items), page_size)
