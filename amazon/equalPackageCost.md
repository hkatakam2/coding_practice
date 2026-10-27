# question
Equal-Cost Warehouse Packages: Given an array itemCost, form the maximum number of packages (each containing 1 or more items) such that every package has the exact same total cost

# clarification
1. max number of packages such that exact same total 
2. 1 is minimum number of packages 
3. verify if a total is possible

# ideas
1. if i make k packages that each cost T, then k * T = Total. So k must divide total, and T = total / k
2. an item can't be split, so T >= max(itemCost). that means k <= total / max(item)
3. k = 1 is always possible. So I can search k from the largest candidate downwards, and the first feasible k is answer

1. bit mask

# outline
maxNumberOfPackages(itemCost):
    total = sum of all costs
    biggest = largest single cost

    for k from (most packages that could possibly work) down to 1:
        if k doesn't divided total: skip
        target = total / k
        if canSplitIntoGroups(itemCost, target): return k

canSplitIntoGroups(items, target):
    fill[mask] = how full the open package is, or "impossible"
    only the empty selection starts as possible (fill 0)
    for each selection(mask) in increasing order:
        skip if impossible
        for each item not yer in the selection:
            if item fits in the open package:
                the selection plus this item becomes possible,
                with fill = fill + item, wrapping to 0 wehen a package closes
    return whether "all items selected" is possible

Three ideas:
1. reachability
2. how full the open package is
3. wrap around when a package closes



# implementation
```python
def max_equal_packages(item_cost):
    total = sum(item_cost)
    biggest = max(item_cost)

    for k in range(min(len(item_cost), total // biggest), 0, -1):
        if total % k != 0:
            continue
        target = total // k

        if can_split_into_groups(item_cost, target):
            return k

def can_split_into_groups(items, target):
    n = len(items)
    full = (1 << n) - 1

    fill = [-1] * (1<<n)
```
canSplitIntoGroups(items, target):
    cost_of[mask] = total cost of the items in the selection
    packable[empty selection] = true

    for each packable selection:
        room_left = space remaining in the open package
        for each item not yet selected:
            if item fits in room_left:
                selection + item is packable

    return whether the fill selection is packable

```python
# backtracking solution instead of bit mask
def can_split_into_groups(items, target):
    # biggest items first: they are the hardest to place, so failures show up early
    items = sorted(items, reverse=True)

    # number of packages needed (total is divisible by target)
    k = sum(items) // target

    # buckets[b] = current cost of package b
    buckets = [0] * k

    def place(i):
        # all items placed -> since total == k * target and nothing overflowed,
        # every package is exactly full
        if i == len(items):
            return True

        already_tried = set()          # skip buckets with identical fill: same outcome
        for b in range(k):
            fits = buckets[b] + items[i] <= target
            if not fits or buckets[b] in already_tried:
                continue
            already_tried.add(buckets[b])

            buckets[b] += items[i]     # try it
            if place(i + 1):
                return True
            buckets[b] -= items[i]     # undo, try the next bucket

        return False                   # no bucket worked for this item

    return place(0)
    
```
    