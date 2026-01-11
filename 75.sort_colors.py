"""
given a list of objects, each with a color,
we need to group objects with the same color; in place
"""


def sort_colors(nums: List[int]):  # nums = [2,0,2,1,1,0]
    # 'left' pointer to where the next 0 should go
    # 'right' pointer to where the next 2 should go
    left = 0
    right = len(nums) - 1
    curr = 0

    # everything after 'right' is already sorted
    while curr <= right:
        # case A: curr is 0
        if nums[curr] == 0:
            # swap it with left
            nums[left], nums[curr] = nums[curr], nums[left]
            # move pointers
            left += 1
            curr += 1

        # case B; curr is 2
        elif nums[curr] == 2:
            # swap it with right
            nums[curr], nums[right] = nums[right], nums[curr]
            # move pointers
            right -= 1
            # don't move curr; it could be 0 or 2

        # case C: curr is 1
        else:
            # don't swap, as 1  needs to be in the middle
            # move curr
            curr += 1
