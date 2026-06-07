# question:
You are given a 2-D matrix `board` containing `'X'` and `'O'` characters.
If a continous, four-directionally connected group of `'O'`s is surrounded by `'X'`s, it is considered to be surrounded.
Change all surrounded regions of `'O'`s to `'X'`s and do so in-place by modifying the input board.

# 1. Restate

Given grid of `'X'`/`'O'`. An `'O'` region (4-dir connected) is "surrounded" if it does NOT touch the border. Flip all surrounded `'O'`s → `'X'`. Modify board in-place.

# 2. Clarifying questions

- Board non-empty? Assume could be empty/single row — handle.
- "Surrounded" = region has no cell on the outer edge of the board. Confirm.
- Diagonal connection counts? No — only up/down/left/right.
- Return value? None, mutate in place.

# 3. Example by hand

```
X X X X
X O O X
X X O X
X O X X
```
- Region {(1,1),(1,2),(2,2)}: none touch border → surrounded → flip.
- Region {(3,1)}: row 3 is last row → touches border → stays.

Result:
```
X X X X
X X X X
X X X X
X O X X
```

# 4. Brainstorm

Direct approach "find each region, check if it touches border" works but bookkeeping per-region is fiddly.

Key flip in thinking: instead of finding surrounded regions, find the **safe** ones. Any `'O'` connected to the border is safe. Everything else is surrounded.

So: start flood-fill from every `'O'` on the border, mark all reachable `'O'`s as safe. Then sweep board — unmarked `'O'` → `'X'`, marked → back to `'O'`.

Complexity: every cell visited O(1) times → O(m·n) time, O(m·n) recursion/stack worst case.

The by-hand method from step 3 (identify regions, test border-contact) is the alternative.

# 5. Solutions

**Option A — Region-based:** For each unvisited `'O'`, collect whole region, check if any cell on border; flip if not. Matches the by-hand step 3.

**Option B — Border flood-fill (reverse):** Mark border-connected `'O'`s as safe, flip the rest. Cleaner because the "surrounded" test becomes implicit.

Both O(m·n). B avoids per-region "did it touch border" tracking — usually easier to get right.

Which would you like to implement?

# 6. Outline

```python
def solve(board):  # -> None (in-place)
    """
    Reframe: don't hunt surrounded O's; mark border-safe O's, flip the rest.
    State: temp marker '#' written onto board itself, chosen because
        an O reachable from any border O can never be surrounded — the
        board doubles as the visited set, no extra structure needed.
    Invariant: after marking, '#' == survives, plain 'O' == surrounded.

    onBorder(r,c) = cell sits on top/bottom/left/right edge.
    markSafe(r,c) = flood-fill from an O, painting connected O's as '#'.

    Core logic:
    - for each border cell that is an O: markSafe it
    - sweep every cell:
        - O  -> X   (was unreachable from border -> surrounded)
        - #  -> O   (restore the safe ones)
    Edge cases:
    - empty board / empty first row -> nothing to do
    - single row or single col -> every O is on border -> all safe
    - markSafe recursion depth on huge all-O board -> may need iterative stack
    """
```

# 7. Iterative implementation

**Iter 1 — skeleton, stubs for helpers:**

```python
def solve(board):
    rows, cols = len(board), len(board[0])

    def on_border(r, c):
        ...  # TODO

    def mark_safe(r, c):
        ...  # TODO flood-fill painting '#'

    # mark all border-connected O's
    for r in range(rows):
        for c in range(cols):
            if on_border(r, c) and board[r][c] == 'O':
                mark_safe(r, c)

    # sweep + flip
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'O':
                board[r][c] = 'X'
            elif board[r][c] == '#':
                board[r][c] = 'O'
```

**Iter 2 — fill `on_border` (easy one first):**

```python
    def on_border(r, c):
        return r == 0 or r == rows - 1 or c == 0 or c == cols - 1
```

**Iter 3 — fill `mark_safe` (recursive flood-fill):**

```python
    def mark_safe(r, c):
        # guard: off-grid or not an unmarked O -> stop
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        if board[r][c] != 'O':
            return
        board[r][c] = '#'               # paint safe
        mark_safe(r + 1, c)             # 4 directions
        mark_safe(r - 1, c)
        mark_safe(r, c + 1)
        mark_safe(r, c - 1)
```

Core logic now complete. Walk edge cases:

**Empty board / empty row** — `len(board[0])` crashes if no rows. Patch at top:

```python
    if not board or not board[0]:
        return
    rows, cols = len(board), len(board[0])
```

**Single row / single col** — every cell satisfies `on_border`, so all O's get marked safe, none flip. Already handled, no change.

**Recursion depth** — fine for typical interview sizes; note the fix below.

Final:

```python
def solve(board):  # -> None, in-place
    if not board or not board[0]:
        return
    rows, cols = len(board), len(board[0])

    def on_border(r, c):
        return r == 0 or r == rows - 1 or c == 0 or c == cols - 1

    def mark_safe(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        if board[r][c] != 'O':
            return
        board[r][c] = '#'
        mark_safe(r + 1, c)
        mark_safe(r - 1, c)
        mark_safe(r, c + 1)
        mark_safe(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if on_border(r, c) and board[r][c] == 'O':
                mark_safe(r, c)

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'O':
                board[r][c] = 'X'
            elif board[r][c] == '#':
                board[r][c] = 'O'
```

# 8. Complexity & optimization

Time O(m·n) — each cell touched O(1) times across marking + sweep. Space O(m·n) recursion stack worst case (board all `'O'`).

Border-scan optimization: only the perimeter can seed `mark_safe`, so replace the full first double-loop with two edge loops (top/bottom rows, left/right cols) — same asymptotics, fewer no-op `on_border` checks:

```python
    for r in range(rows):
        mark_safe(r, 0); mark_safe(r, cols - 1)
    for c in range(cols):
        mark_safe(0, c); mark_safe(rows - 1, c)
```

Stack-overflow fix for the recursion-depth edge case: swap recursion for an explicit stack.

```python
    def mark_safe(sr, sc):
        stack = [(sr, sc)]
        while stack:
            r, c = stack.pop()
            if r < 0 or r >= rows or c < 0 or c >= cols: continue
            if board[r][c] != 'O': continue
            board[r][c] = '#'
            stack += [(r+1,c), (r-1,c), (r,c+1), (r,c-1)]
```