"""
facts:
    m = 3.28 ft
    ft = 12 in
    hr = 60 min
    min = 60 sec

example query:
    2 m = ?-in -->• answer = 78.72
    13 in = ? m •--> answer = 0.330 (roughly)
    13 in•= ? hr •--> "not convertiblel"

clearly these releationships is a graph
reverse conversion, double edged graph with different weights

once we have graph, then we need to do BFS, until we reach target node


"""

from collections import defaultdict, deque


def solve_conversions(facts, queries):
    # 1. build graph
    # graph structure: {'unit': [('neighbor_unit', rate)]}
    facts_graph = defaultdict(list)

    for fact in facts:
        # fact format: ("m", "ft", 3.28)
        u_from, u_to, rate = fact
        facts_graph[u_from].append((u_to, rate))
        facts_graph[u_to].append((u_from, 1.0 / rate))

    # 2. process queries
    results = []
    for val, start_unit, end_unit in queries:
        # edge cases
        if start_unit not in facts_graph or end_unit not in facts_graph:
            results.append("not convertible")
            continue

        if start_unit == end_unit:
            results.append(val)
            continue

        # BFS to reach end_unit from start_unit
        queue = deque([(start_unit, val)])
        visited = set()
        found = False
        while queue:
            current_unit, current_val = queue.popleft()

            # did we reach target?
            if current_unit == end_unit:
                results.append(current_val)
                found = True
                break

            # look at neighbors
            for neighbor_unit, rate in facts_graph[current_unit]:
                if neighbor_unit not in visited:
                    visited.add(neighbor_unit)
                    queue.append((neighbor_unit, current_val * rate))

        if not found:
            results.append("not convertible")
    return results


# --- TESTING THE CODE ---

# Input Facts
facts = [
    ("m", "ft", 3.28),
    ("ft", "in", 12.0),
    ("hr", "min", 60.0),
    ("min", "sec", 60.0),
]

# Input Queries
queries = [
    (2.0, "m", "in"),  # 2 meters to inches
    (13.0, "in", "m"),  # 13 inches to meters
    (13.0, "in", "hr"),  # 13 inches to hours
]

output = solve_conversions(facts, queries)

for q, ans in zip(queries, output):
    print(f"{q[0]} {q[1]} -> {q[2]} : {ans}")
