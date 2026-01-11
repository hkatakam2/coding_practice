"""
given an mXn matrix mat, return the distance of the nearestest 0 for each cell
"""

from collections import deque
from typing import List


def distanceMatrix(mat: List[List[int]]) -> List[List[int]]:
    rows, cols = len(mat), len(mat[0])

    dist = [[-1] * cols for _ in range(rows)]  # -1 as impossible distance

    # collecting all 0 cells as source points and finding distances as a flood flow
    queue = deque()

    for r in range(rows):
        for c in range(cols):
            if mat[r][c] == 0:
                queue.append((r, c))
                dist[r][c] = 0

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    while queue:
        r, c = queue.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] == -1:
                dist[nr][nc] = 1 + dist[r][c]
                queue.append((nr, nc))
    return dist
