from collections import defaultdict


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, i):
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i != root_j:
            # union by size
            if self.size[root_i] < self.size[root_j]:
                root_i, root_j = root_j, root_i
            self.parent[root_j] = root_i
            self.size[root_i] += self.size[root_j]
            return True
        return False


class Solution:
    def minMalwareSpread(self, graph, initial) -> int:
        n = len(graph)
        initial_set = set(initial)
        clean_nodes = [i for i in range(n) if i not in initial_set]

        # 1. group all CLEAN nodes into components
        dsu = self._build_clean_components(n, graph, clean_nodes)

        # 2. analyze how infected nodes connect to these clean components
        # source_to_components: {infected_node_u : {root1, root2, ...}}
        # component_threats: {root1: count_of_infected_sources}
        source_to_components, component_threats = self._map_infections(
            n, graph, initial_set, dsu
        )

        # 3. find the node that saves most lives
        return self._find_best_removal(
            initial, source_to_components, component_threats, dsu
        )

    def _build_clean_components(self, n: int, graph, clean_nodes) -> UnionFind:
        dsu = UnionFind(n)
        for i in clean_nodes:
            for j in clean_nodes:
                if i < j and graph[i][j] == 1:
                    dsu.union(i, j)
        return dsu

    def _map_infections(self, n, graph, initial_set, dsu):
        source_to_components = defaultdict(set)
        component_threats = defaultdict(int)

        for u in initial_set:
            for v in range(n):
                # 1. connected? 2. is neighbor v actually clean?
                if graph[u][v] == 1 and v not in initial_set:
                    root_v = dsu.find(v)
                    if root_v not in source_to_components[u]:
                        source_to_components[u].add(root_v)
                        component_threats[root_v] += 1
        return source_to_components, component_threats

    def _find_best_removal(self, initial, source_to_components, component_threats, dsu):
        best_node = -1
        max_saved = -1

        # sorting ensures we return the smallest index in case of a tie
        for u in sorted(initial):
            saved = 0
            for root in source_to_components[u]:
                # we only save a component if u is the ONLY threat
                if component_threats[root] == 1:
                    saved += dsu.size[root]
            if saved > max_saved:
                max_saved = saved
                best_node = u

        return best_node
