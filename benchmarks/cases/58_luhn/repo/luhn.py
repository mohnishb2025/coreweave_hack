def valid(number):
    return sum(int(digit) for digit in number) % 10 == 0
