"""
given array of heights of bars, each bar width =1. return the area of largest rectangle

"""

from typing import List


# idea: use stack; If the current bar is smaller, pop the tall ones and calculate area
def largest_rectangle(heights: List[int]) -> int:
    max_area = 0
    stack = []

    for i, curr_height in enumerate(heights):
        while stack and heights[stack[-1]] > curr_height:
            height = heights[stack.pop()]

            # what if stack is now empty?
            width = i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)
    # what if loop is done but stack is not empty at the end, there are bars left?
    return max_area
