class Queue_10:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        if len(self.items) > 9:
            self.items.pop()

        self.items.insert(0,item)

    def val(self):
        return self.items

    def size(self):
        return len(self.items)
