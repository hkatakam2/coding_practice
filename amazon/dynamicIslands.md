# question
Dynamic Number of Islands (Number of Islands II - LeetCode 305): Given a grid where obstacles or active nodes are added dynamically via queries, return the connected component count after each query using

# clarifications
we start with m*n grid of water. each query makes a cell land, we have to return the number of islands after each query.

We start with an m x n grid of water. Each query turns one water cell into land. After each query, I report how many islands exist. An island is a group of land cells connected up, down, left, or right (not diagonally).

So the output is a list with one island count per query, in query order.

1. connectivity 4 directions
2. can a query repeat a cell? yes, no change in outpu
3. can a query be out of bounds? no, be defensive
4. can a land be removed? No

# ideas
1. brute force: after every query we can run a BFS/DFS but it will be slow
2. update locally. A new land can only effect the 4 neighbors. before query they belong to different islands, after query they belong to 1 island. 
   1. island count changes by +1 for the new island; -1 each for the islands it joins together
3. we can use union find to do this cheaply

# outline
number_of_islands_after_each_query(grid size, queries):
    island_count = 0
    for each query cell:
        make cell land (its own island); island_count += 1
        for each neighbor of cell:
            if neighbor is land:
                union(cell, neighbor)
                if union joined two different islands: island_count -= 1
        record island_count
    return all recorded island_counts

```python
def number_of_islands_after_each_query(m, n, queries):
    # island_count = 0
    island_count = 0
    counts = []

    # for each query cell:
    for r, c in queries:
        # make cell land (its own island); island_count += 1
        make_land(r, c)                          # STUB
        island_count += 1

        # for each neighbor of cell:
        for nr, nc in neighbors_of(r, c):        # STUB
            # if neighbor is land:
            if is_land(nr, nc):                  # STUB
                # union(cell, neighbor)
                # if union joined two different islands: island_count -= 1
                if union((r, c), (nr, nc)):      # STUB
                    island_count -= 1

        # record island_count
        counts.append(island_count)

    # return all recorded island_counts
    return counts

# iteration 1

class UnionFind:                                 # STUB, next iteration
    def __init__(self, size): ...
    def union(self, a, b): ...                   # True if it joined two different islands


def number_of_islands_after_each_query(m, n, queries):
    union_find = UnionFind(m * n)                # new: union needs somewhere to live
    land = set()                                 # new: cells that are land
    island_count = 0
    counts = []

    def cell_id(r, c):                           # new: UnionFind wants one integer per cell
        return r * n + c

    def neighbors_of(r, c):
        return [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]

    for r, c in queries:
        # make cell land (its own island); island_count += 1
        land.add((r, c))
        island_count += 1

        # for each neighbor of cell:
        for nr, nc in neighbors_of(r, c):
            # if neighbor is land:
            if (nr, nc) in land:
                # union(cell, neighbor); if union joined two different islands: -1
                if union_find.union(cell_id(r, c), cell_id(nr, nc)):
                    island_count -= 1

        # record island_count
        counts.append(island_count)

    # return all recorded island_counts
    return counts

# iteration 2
class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))          # every cell starts as its own island

    def find(self, x):
        while self.parent[x] != x:
            x = self.parent[x]
        return x

    def union(self, a, b):
        root_a, root_b = self.find(a), self.find(b)
        if root_a == root_b:
            return False                         # already the same island
        self.parent[root_b] = root_a
        return True

```
# edge cases
```python
class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.size = [1] * size

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        root_a, root_b = self.find(a), self.find(b)
        if root_a == root_b:
            return False
        if self.size[root_a] < self.size[root_b]:
            root_a, root_b = root_b, root_a
        self.parent[root_b] = root_a
        self.size[root_a] += self.size[root_b]
        return True


def number_of_islands_after_each_query(m, n, queries):
    union_find = UnionFind(m * n)
    land = set()
    island_count = 0
    counts = []

    def cell_id(r, c):
        return r * n + c

    def neighbors_of(r, c):
        return [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]

    for r, c in queries:
        # EDGE: out-of-bounds query or already-land cell -> nothing changes
        if not (0 <= r < m and 0 <= c < n) or (r, c) in land:
            counts.append(island_count)
            continue

        # make cell land (its own island); island_count += 1
        land.add((r, c))
        island_count += 1

        # for each neighbor of cell:
        for nr, nc in neighbors_of(r, c):
            # if neighbor is land:   (out-of-bounds neighbors are never in `land`)
            if (nr, nc) in land:
                # union(cell, neighbor); if union joined two different islands: -1
                # (two neighbors on the same island -> second union returns False)
                if union_find.union(cell_id(r, c), cell_id(nr, nc)):
                    island_count -= 1

        # record island_count
        counts.append(island_count)

    # return all recorded island_counts
    return counts


print(number_of_islands_after_each_query(
    3, 3, [(0, 0), (0, 1), (1, 2), (2, 1)]))             # [1, 1, 2, 3]
print(number_of_islands_after_each_query(
    3, 3, [(0, 0), (0, 2), (1, 1), (0, 1), (1, 0)]))     # [1, 2, 3, 1, 1]
print(number_of_islands_after_each_query(1, 1, [(0, 0), (0, 0)]))   # [1, 1]
print(number_of_islands_after_each_query(2, 2, [(5, 5), (0, 0)]))   # [0, 1]
print(number_of_islands_after_each_query(3, 3, []))                 # []
print(number_of_islands_after_each_query(0, 0, [(0, 0)]))           # [0]
```