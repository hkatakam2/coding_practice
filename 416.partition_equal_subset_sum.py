"""
given an int array; return if you can partition the array into two equal subsets.

aha! you need to find elemets that add upto sum / 2
"""


def partition_subsets(nums: List[int]) -> bool:
    total_sum = sum(nums)
    if total_sum % 2 != 0:  # exit early; can't divide odd sum
        return False

    target = total_sum // 2

    memo = {}  # keys are (index, current_target)

    def dfs(index, current_target):
        if current_target == 0:
            return True

        if current_target < 0 or index > len(nums) - 1:
            return False

        # check cache
        if (index, current_target) in memo:
            return memo[(index, current_target)]

        # choice either choose the current num or skip it
        res = dfs(index + 1, current_target - nums[index]) or dfs(
            index + 1, current_target
        )
        memo[(index, current_target)] = res  # store it before returning
        return res

    return dfs(0, target)
