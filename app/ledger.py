from collections import Counter


class Ledger:
    def __init__(self):
        self.ints = []
        self.floats = []
        self.strings = []

    def insert(self, item):
        if type(item) is int:
            self.ints.append(item)
        elif type(item) is float:
            self.floats.append(item)
        elif type(item) is str:
            self.strings.append(item)
        else:
            raise TypeError("Item is not supported by the ledger")

    def get_count(self, item):
        if type(item) is int:
            c = Counter(self.ints)
        elif type(item) is float:
            c = Counter(self.floats)
        elif type(item) is str:
            c = Counter(self.strings)
        else:
            raise TypeError(f"Type is not tracked by the ledger:{item}.")
        return c[item]

    def get_avg(self, d_type):
        dividend = 0
        divisor = 0
        if d_type == 'ints':
            for item in self.ints:
                dividend += item
                divisor = len(self.ints)

        elif d_type == 'floats':
            for item in self.floats:
                dividend += item
                divisor = len(self.floats)
        else:
            raise TypeError(f"Type is not tracked by the ledger:{d_type}.")
        try:
            return dividend / divisor
        except ZeroDivisionError:
            raise ZeroDivisionError(f"Ledger {d_type} is empty")