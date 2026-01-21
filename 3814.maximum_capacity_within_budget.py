"""
You are given two integer arrays costs and capacity, both of length n, where costs[i] represents the purchase cost of the ith machine and capacity[i] represents its performance capacity.

You are also given an integer budget.

You may select at most two distinct machines such that the total cost of the selected machines is strictly less than budget.

Return the maximum achievable total capacity of the selected machines.
"""

from typing import List


class Solution:
    def maxCapacity(self, costs: List[int], capacity: List[int], budget: int) -> int:
        n = len(costs)
        # 1. Combine and Sort by cost
        # We zip them to keep cost and capacity linked, then sort.
        machines = sorted(zip(costs, capacity))

        # Unzip into separate lists for easier access
        sorted_costs = [m[0] for m in machines]
        sorted_caps = [m[1] for m in machines]

        # 2. Precompute Prefix Maximum Capacity
        # prefix_max[i] will store the max capacity found in machines[0...i]
        prefix_max = [0] * n
        current_max = 0
        for i in range(n):
            current_max = max(current_max, sorted_caps[i])
            prefix_max[i] = current_max

        max_capacity = 0

        import bisect

        # 3. Iterate through each machine and find its best pair
        for i in range(n):
            cost_i = sorted_costs[i]
            cap_i = sorted_caps[i]

            # Case A: Pick ONLY this machine (must be strictly less than budget)
            if cost_i < budget:
                max_capacity = max(max_capacity, cap_i)
            else:
                # Since costs are sorted, if this cost >= budget, subsequent ones will be too.
                # We can stop early.
                break

            # Case B: Pick this machine + one other machine
            # We need: cost_j < budget - cost_i
            remaining_budget = budget - cost_i

            # Binary search to find the rightmost index where cost < remaining_budget
            # bisect_left returns the first index where value >= remaining_budget
            # so subtracting 1 gives us the index where value < remaining_budget.
            idx = bisect.bisect_left(sorted_costs, remaining_budget) - 1

            # We must ensure we pick a DISTINCT machine.
            # By only looking at indices strictly less than 'i', we ensure distinctness
            # and avoid double counting.
            search_limit = min(i - 1, idx)

            if search_limit >= 0:
                # prefix_max[search_limit] gives the best capacity among all valid partners
                best_partner_capacity = prefix_max[search_limit]
                max_capacity = max(max_capacity, cap_i + best_partner_capacity)

        return max_capacity
