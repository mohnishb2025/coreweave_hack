def distance(left, right):
    return sum(a != b for a, b in zip(left, right)) + abs(len(left) - len(right))
