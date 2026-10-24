# question
Minimum/Maximum Partition Cost: Given an array of server loads/weights and an integer $k$, partition the array into $k$ contiguous subarrays where the cost of a split between index $i-1$ and $i$ is arr[i-1] + arr[i]. Return both the minimum and maximum possible total partition costs 

# clarifications

# ideas
1. build n-1 split sums and choose k-1 of them
   1. minTotal = smallest k-1 split sums
   2. maxTotal = largest k-1 split sums


# outline
partition_cost_range(arr, k):
    split_costs = cost_of_every_split(arr)
    sort split costs
    picks = k-1
    min_cost = sum of picks smallest k-1
    max-cost = sum of picks largest k-1
    return (min_cost, max_cost)

```python
def partition_cost_range(arr, k):
    split_costs = [arr[i-1] + arr[i] for i in range(1, len(arr))]
    split_costs.sort()

    picks = k-1
    min_cost = sum(split_costs[:picks])
    max_cost = sum(split_costs[len(split_costs) - picks:])

    return (min_cost, max_cost)

```

# edge cases
```python
def partition_cost_range(arr, k):
    n = len(arr)

    # reject invalid input
    if n == 0 or k < 1 or k > n:                       # EDGE: empty, bad k, k > n
        raise ValueError("Need 1 <= k <= len(arr) and a non-empty array")
    if k == 1:                                         # EDGE: no splits -> no cost
        return 0, 0

    # split_costs = cost_of_every_split(arr)           # n-1 values: arr[i-1] + arr[i]
    split_costs = [arr[i - 1] + arr[i] for i in range(1, n)]

    # sort split_costs
    split_costs.sort()

    # picks = k - 1                                    # how many splits we must make
    picks = k - 1

    # min_cost = sum of the `picks` smallest
    min_cost = sum(split_costs[:picks])

    # max_cost = sum of the `picks` largest
    # EDGE: use len - picks, NOT [-picks:] (since -0 would grab everything)
    max_cost = sum(split_costs[len(split_costs) - picks:])

    # return (min_cost, max_cost)
    return min_cost, max_cost


# Sanity checks
assert partition_cost_range([1, 3, 5, 1], 3) == (10, 14)
assert partition_cost_range([1, 3, 5, 1], 1) == (0, 0)
assert partition_cost_range([1, 3, 5, 1], 4) == (18, 18)   # k == n: all splits
assert partition_cost_range([7], 1) == (0, 0)
assert partition_cost_range([-2, 4, -6, 1], 2) == (-5, 2)  # negatives
```