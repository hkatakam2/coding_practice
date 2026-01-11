"""
design a data structure that can store multiple values for the same key at different time stamps

set(key, value, timestamp); always set timestamps are increasing; store multiple
get(key, timestamp) ; get the value that is at the timestamp and just earlier
"""


class TimeStamp:
    def __init__(self):
        self.store = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        if key not in self.store:
            self.store[key] = []
        # just append in both cases
        self.store[key].append([value, timestamp])

    def get(self, key: str, timestamp: int) -> str:
        res = ""
        values = self.store[key]

        # as timestamps are sorted, use binary search
        left, right = 0, len(values) - 1
        while left <= right:
            mid = (left + right) // 2
            if values[mid][1] <= timestamp:
                res = values[mid][0]  # possible value
                left = mid + 1
            else:
                right = mid - 1
        return res
