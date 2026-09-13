class LRU:
    def __init__(self, capacity):
        self.capacity = capacity
        self.data = {}
        self.order = []

    def get(self, key):
        return self.data[key]

    def put(self, key, value):
        if key in self.data:
            self.data[key] = value
            return
        if len(self.data) >= self.capacity:
            oldest = self.order.pop(0)
            del self.data[oldest]
        self.data[key] = value
        self.order.append(key)
