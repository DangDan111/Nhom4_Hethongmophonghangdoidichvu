class LinearQueue:
    def __init__(self, max_size=50):
        self.max_size = max_size
        self.items = []
        self.front = 0

    def enqueue(self, item):
        if self.is_full():
            return False
        self.items.append(item)
        return True

    def dequeue(self):
        if self.is_empty():
            return None
        item = self.items[self.front]
        self.front += 1
        if self.front > 10 and self.front * 2 >= len(self.items):
            self.items = self.items[self.front:]
            self.front = 0
        return item

    def is_empty(self):
        return self.size() == 0

    def is_full(self):
        return self.size() >= self.max_size

    def size(self):
        return len(self.items) - self.front

    def to_list(self):
        return self.items[self.front:].copy()
