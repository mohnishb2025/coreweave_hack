def valid(isbn):
    digits = [int(char) for char in isbn if char.isdigit()]
    return sum(digits) % 10 == 0
