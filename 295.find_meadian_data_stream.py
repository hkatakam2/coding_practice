"""
data is streaming, we need to efficiently calculate the running median

aha! we care about median only; not the order
use two heaps first_half, second_half
"""


class MedianFinder:
    def __init__(self):
        self.first_half = []  # max_heap
        self.second_half = []  # min_heap

    def addNum(self, num: int) -> None:
        # always add to the first_half
        heapq.heappush_max(self.first_half, num)
        # get the max of first half
        max_of_first_half = heapq.heappop_max(self.first_half)
        # push it to second half
        heapq.heappush(self.second_half, max_of_first_half)

        # if second half has more items; pop the min of second half
        # push it to first half; so always first half is equal or 1 more than second half
        if len(self.second_half) > len(self.first_half):
            min_second_half = heapq.heappop(self.second_half)
            heapq.heappush_max(self.first_half, min_second_half)

    def findMedian(self) -> float:
        if len(self.first_half) > len(self.second_half):s
            return self.first_half[-1]
        else:
            return (self.first_half + self.second_half) / 2.0
