'''
given an undirected graph with maximum degree D, find a graph coloring
using at most D+1 colors

graphs are represented by a list of N node objects, each with a label,
a set of neighbors, and a color
'''
class GraphNode:
    def __init__(self, label):
        self.label = label
        self.neighbors = set()
        self.color = None

a = GraphNode('a')
b = GraphNode('b')
c = GraphNode('c')

a.neighbors.add(b)
b.neighbors.add(a)
b.neighbors.add(c)
c.neighbors.add(b)

graph = [a, b, c]
'''
brute force: try each possible combination of colors until we find a legal coloring
1. for each possible coloring
2. if the coloring is legal, then return it
3. else, move of to the next coloring

O(D^N) colorings and we need to check M edges too

how to do better?
instead of assigning all the colors at once, what if we colored the nodes
one by one

we could assign a color for the first node, then find a legal color for
the second node, then for the third node, and keep going node by node
'''
def color_graph(graph, colors):
    for node in graph:
        # get the node's neighbors colors, as a set so we can
        # check if a color is illegal in constant time
        illegal_colors = set([
            neighbor.color for neighbor in node.neighbors if neighbor.color
        ])
        legal_colors = [
            color for color in colors if color not in illegal_colors
        ]
        # assign the first legal color
        node.color = legal_colors[0]
'''
will we run out of legal colors?
"Each node has at most D neighbors, and we have D + 1 colors. So, if 
we look at any node, there's always at least one color that's not 
taken by its neighbors."

We're iterating through each node in the graph, so the loop body executes N times. In each iteration of the loop:
1. We look at the current node's neighbors to figure out what colors are already taken.
That's O(D), since any given node can have up to D neighbors.
2. Then, we look at all the colors (there are O(D) of them) to see which ones are available.
3. Finally, we pick the first color that's free and assign it to the node (O(1)).
So our runtime is N * (D + D + 1), which is O(N * D).

in step 2:
When we're coloring a node, we just need one color that hasn't been 
taken by any of the node's neighbors. We can stop looking at colors 
as soon as we find one:
'''
def color_graph(graph, colors):
    for node in graph:
        # get the neigbors colors as a set of illegal_colors
        illegal_colors = set([
            neighbor.color for neighbor in node.neighbors if neighbor.color
        ])

        # assign the first legal color
        for color in colors:
            if color not in illegal_colors:
                node.color = color
                break
'''
O(N + M) time, we have to look at every node and every edge
O(D) additional space

are there any edge cases? (generally for graph)
1. nodes with no edges (isolated nodes with no edges)
2. cycles
3. loops (a node that is adjacent to itself)

our function works in cases 1, 2
with 3 it's impossible to find a legal color, so should throw an error

how do we detect loops?
'''
def color_graph(graph, colors):
    for node in graph:
        if node in node.neighbors:
            raise Exception('Legal coloring impossible \
                            for node with loop: %s' % node.label)
        # get the node's neighbors colors, as a set so we
        # can check if a color is illegal in constant time
        illegal_colors = set([
            neighbor.color for neighbor in node.neighbors if neighbor.color
        ])  

        # assign the first legal color
        for color in colors:
            if color not in illegal_colors:
                node.color = color
                break
'''
O(N + M) time? think in terms of edges we are checking
O(D) space

Bonus:
1. Our solution runs in O(N + M) time but takes O(D) space. 
Can we get down to O (1) space?

'''  
def color_graph(graph, colors):
    for node in graph:
        # check for loops
        if node in node.neighbors:
            raise Exception(f'Legal coloring impossible for node with loop: {node.label}')

        # instead of strong colors in a set, check neighbors directly
        for color in colors:
            # assume color is legal until we find a neighbor with same color
            color_is_legal = True
            
            # check each neighbor's color
            for neighbor in node.neighbors:
                if neighbor.color == color:
                    color_is_legal = False
                    break
            
            # if we found a legal color, use it and move to next node
            if color_is_legal:
                node.color = color
                break
'''
O(N + M) time
O(1) additional space

what we learned?
we used greedy solution



bonus: 
2. Our solution finds a legal coloring, but there are usually many 
legal colorings. What if we wanted to optimize a coloring to use as 
few colors as possible?

The problem of determining if a graph can be colored with k colors is 
in the class of problems called NP (nondeterministic polynomial time). 
This means that in polynomial time, we can verify a solution is correct 
but we can't come up with a solution. In this case, if we have a graph 
that's already colored with k colors we verify the coloring uses k colors 
and is legal, but we can't take a graph and a number k and determine if 
the graph can be colored with k colors.

One way to reliably reduce the number of colors we use is to use the 
greedy algorithm but carefully order the nodes. For example, we can 
prioritize nodes based on their degree, the number of colored neighbors 
they have, or the number of uniquely colored neighbors they have.

'''
def optimize_graph_coloring(graph, max_colors):
    """
    Optimize graph coloring to use minimum colors possible.
    Uses degree-based ordering and greedy approach.
    """
    # Sort nodes by degree (number of neighbors) in descending order
    nodes_by_degree = sorted(
        graph,
        key=lambda node: len(node.neighbors),
        reverse=True
    )
    
    # Try coloring with increasing number of colors
    for num_colors in range(1, max_colors + 1):
        colors = list(range(num_colors))
        
        # Reset colors
        for node in nodes_by_degree:
            node.color = None
            
        try:
            # Try to color with current number of colors
            for node in nodes_by_degree:
                # Find first legal color
                color_found = False
                for color in colors:
                    if is_color_legal(node, color):
                        node.color = color
                        color_found = True
                        break
                
                if not color_found:
                    raise ValueError("Need more colors")
                    
            # If we succeed, return current number of colors
            return num_colors
            
        except ValueError:
            # If coloring fails, try with more colors
            continue
    
    # reaching here means we could not color even with max_colors, this won't happen
    raise ValueError(f"Could not color graph with {max_colors} colors")

def is_color_legal(node, color):
    """Check if a color is legal for a node."""
    return not any(
        neighbor.color == color 
        for neighbor in node.neighbors
    )

# Helper function to test the coloring
def verify_coloring(graph):
    """Verify that the graph is legally colored."""
    used_colors = set()
    
    for node in graph:
        # Check if node has a color
        if node.color is None:
            return False
            
        # Track used colors
        used_colors.add(node.color)
        
        # Check neighbors
        for neighbor in node.neighbors:
            if neighbor.color == node.color:
                return False
                
    return len(used_colors)

# example usage
# Test the optimized coloring
def test_optimized_coloring():
    # Create test graph
    a = GraphNode('a')
    b = GraphNode('b')
    c = GraphNode('c')
    d = GraphNode('d')
    
    # Create edges
    a.neighbors.add(b)
    b.neighbors.add(a)
    b.neighbors.add(c)
    c.neighbors.add(b)
    c.neighbors.add(d)
    d.neighbors.add(c)
    
    graph = [a, b, c, d]
    
    # Try to color with minimum colors
    max_colors = len(graph)
    colors_used = optimize_graph_coloring(graph, max_colors)
    
    # Verify and print results
    is_valid = verify_coloring(graph)
    print(f"Colors used: {colors_used}")
    print(f"Valid coloring: {is_valid}")
    for node in graph:
        print(f"Node {node.label}: Color {node.color}")

# Run test
test_optimized_coloring()

'''
Key features of this implementation:

Degree-Based Ordering:

Nodes with more neighbors are colored first
This often leads to better color utilization

Incremental Color Testing:

Starts with minimum colors (1)
Incrementally tries more colors until successful

Verification:

Includes helper function to verify legal coloring
Tracks number of colors actually used

Space Efficiency:

Uses O(N) additional space for sorting
Could be optimized further if needed
While this doesn't guarantee the absolute minimum number of colors, it 
often produces better results than the basic greedy approach.
'''


