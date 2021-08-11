import math
from collections import defaultdict


class Ledger:
    def __init__(self):
        self.ints = defaultdict(int)
        self.floats = defaultdict(int)
        self.strings = defaultdict(int)

    def get_count(self, item):
        if type(item) is int:
            return self.ints[item]
        elif type(item) is float:
            return self.floats[item]
        elif type(item) is str:
            return self.strings[item]
        else:
            raise TypeError(f"Type is not tracked by the ledger:{item}.")

    def get_avg(self, d_type):
        dividend = 0
        # since we track the occurrences of the numbers in a defaultdict, the divisor is the sum of their values.
        divisor = 0
        if d_type == 'ints':
            for k, v in self.ints.items():
                dividend += int(k) * int(v)
                divisor += v

        elif d_type == 'floats':
            for k, v in self.ints.items():
                dividend += float(k) * float(v)
                divisor += v
        else:
            raise TypeError(f"Type is not tracked by the ledger:{d_type}.")
        try:
            return dividend / divisor
        except ZeroDivisionError:
            raise ZeroDivisionError(f"Ledger {d_type} is empty")
