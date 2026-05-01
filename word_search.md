"""
Given an m x n grid of characters board and a string word, return true if word exists in the grid.
"""
```python
class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        rows, cols = len(board), len(board[0])
        visited = set()

        # This is the "find_next" you were trying to write!
        def dfs(r, c, index):
            # TODO 1: Base cases (Did we win? Are we out of bounds? Wrong letter? Already visited?)
            
            # TODO 2: Mark current cell as visited
            
            # TODO 3: Search all 4 directions recursively
            
            # TODO 4: BACKTRACK! Un-mark the cell so other paths can use it
            
            # TODO 5: Return whether any of the 4 directions worked
            pass

        # Start the process
        for r in range(rows):
            for c in range(cols):
                # If we find the first letter, kick off the recursive search
                if board[r][c] == word[0]:
                    if dfs(r, c, 0):
                        return True
                        
        return False
```
State for our recursive function. At any exact moment in our search, what do we need to know?
- Where are we? (r, c)
- What character are we looking for? (index of the word)
- Where have we been? (visited set)

Approach:
To solve this, I'll iterate through the board to find the first character of the word. Once found, I will use a recursive Depth-First Search (DFS) to explore the adjacent cells. To handle the state of our path, I'll pass the current row, column, and word index into the DFS. I will also maintain a visited set. If a path reaches a dead end, I will backtrack by removing the current cell from the visited set before returning from the recursive call. This ensures we don't reuse cells in a single path, but leaves them available for other paths
