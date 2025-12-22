"""
given array of heights of bars, each bar width =1. return the area of largest rectangle

"""

from typing import List


# idea: use stack; If the current bar is smaller, pop the tall ones and calculate area
def largest_rectangle(heights: List[int]) -> int:
    heights.append(0)  # to force the stack to empty at the end
    max_area = 0
    stack = [-1]  # to handle the left boundary of the first bar

    for i, curr_height in enumerate(heights):
        while stack[-1] != -1 and heights[stack[-1]] > curr_height:
            # 1. pop top element, height of rectangle
            height = heights[stack.pop()]

            # 2. right boundary is the current index i
            # 3. left boundary is the "new" top of the stack
            width = i - stack[-1] - 1

            max_area = max(max_area, height * width)
        stack.append(i)
    return max_area
