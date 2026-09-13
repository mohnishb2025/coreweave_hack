class Ring:
    def __init__(self, capacity):
        self.buf = [None] * capacity
        self.cap = capacity
        self.head = 0
        self.tail = 0

    def push(self, item):
        self.buf[self.tail] = item
        self.tail = (self.tail + 1) % self.cap

    def pop(self):
        item = self.buf[self.head]
        self.head = (self.head + 1) % self.cap
        return item

    def empty(self):
        return self.head == self.tail
