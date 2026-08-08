'''
cycle in a linked list

class LinkedListNode(object):
    def __init__(self, value):
        self.value = value
        self.next = None

write a function contains_cycle() that takes the first node in a singly
linked list and returns a boolean indicating whether the list contains a cycle.

we can store already seen nodes in a set, 
looped list run forever. how will we tell we've run into a loop?

one way is to look for landmarks. you could remember one specific point
and if you pass that point again, you know you're running a loop

Well, our cycle can occur after a non-cyclical "head" section in the 
beginning of our linked list. So we'd need to make sure we chose 
a "landmark" node that is in the cyclical "tail" and not in the 
non-cyclical "head." That seems impossible unless we already know 
whether or not there's a cycle...

Besides landmarks, what are some other ways you could tell you're 
running in a loop? What if you had another runner? "Remember, 
it's a singly-linked list, so no running backwards!)

A tempting approach could be to have the other runner stop and act as 
a "landmark," and see if you pass her again. But we still have the 
problem of making sure our "landmark" is in the loop and not in the 
non-looping beginning of the trail.
What if our "landmark" runner moves continuously but slowly?
'''
def contains_cycle(first_node):
    # start both runners at the beginning
    slow_runner = first_node
    fast_runner = first_node

    # until we hit the end of the list
    while fast_runner is not None and fast_runner.next is not None:
        slow_runner = slow_runner.next
        fast_runner = fast_runner.next.next

        # case: fast_runner is about to lap slow_runner
        if fast_runner is slow_runner:
            return True
        
    # case fast_runner hit the end of the list
    return False
'''
O(n) time and O(1) space

Bonus: How would you detect the first node in the cycle? Define the 
first node of the cycle as the one closest to the head of the list.

clue: the distance from the head to the cycle start equals the distance from 
the meeting point to the cycle start when traversing in the cycle.
'''
def find_first_node_in_cycle(first_node):
    slow_runner = first_node
    fast_runner = first_node

    # detect if there is a cycle
    while fast_runner is not None and fast_runner.next is not None:
        slow_runner = slow_runner.next
        fast_runner = fast_runner.next

        # cycle detected
        if slow_runner is fast_runner: # we are checking for identity
            # reset one runner to the head
            slow_runner = first_node
            while slow_runner != fast_runner: # we are checking node values/references. not checking for identity
                slow_runner = slow_runner.next
                fast_runner = fast_runner.next
            return slow_runner # first node in the cycle
    # no cycle
    return None
'''
Bonus: would the code work if fast runner moves 3 steps every time
No, the fast runner could skip over
you need to have additional checks at each step
'''
'''
Bonus: detecting cycles in a directed graph. each node has multiple next
pointers instead of just 1

we can use dfs with a visited status for each node: not visited, visiting and visited
	•	Not Visited: The node hasnt been traversed yet.
	•	Visiting: The node is currently being visited (part of the current DFS path).
	•	Visited: The node and all its descendants have been fully explored.

'''
def has_cycle_in_directed_graph(graph):
    def dfs(node, visiting, visited):
        if node in visiting: # cycle detected
            return True
        if node in visited: # already fully processed
            return False
        
        # mark the node as visiting
        visiting.add(node)

        # recur for all adjacent nodes
        for neighbor in graph[node]:
            if dfs(neighbor, visiting, visited):
                return True
        # move the node from 'visiting to visited
        visiting.remove(node)
        visited.add(node)
        return False

    visiting = set()
    visited = set()

    # check all nodes in the graph
    for node in graph:
        if dfs(node, visiting, visited):
            return True
    return False
# O(V+E) time and O(V) space
