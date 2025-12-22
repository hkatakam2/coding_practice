"""
given array of heights of bars, each bar width =1. return the area of largest rectangle

"""

from typing import List


def largest_rectangle(heights: List[int]) -> int:
    max_area = 0
    n = len(heights)
    for i in range(n):
        curr_height = heights[i]

        # 1. expand to the left
        left = i
        while left > 0 and heights[left - 1] >= curr_height:
            left -= 1

        # 2. exaand to the right
        right = i
        while right < n - 1 and heights[right + 1] >= curr_height:
            right += 1

        # 3. calculate area
        width = left - right + 1
        max_area = max(max_area, width * curr_height)
    return max_area
