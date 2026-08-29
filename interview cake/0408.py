'''
Given information about active users on the network, find the shortest route for a message from one user (the sender) to another (the recipient). 
Return a list of users that make up this route.

there might be many shortest routes, just return any shortest route.

Your network information takes the form of a dictionary mapping username strings to a list of other users nearby:
network = {
    'Min' : ['William', 'Jayden', 'Omar'],
    'William' : ['Min', 'Noam'],
    'Jayden' : ['Min', 'Amelia', 'Ren', 'Noam'], 
    'Ren': ['Jayden', 'Omar'],
    'Amelia' : ['Jayden', 'Adam', 'Miguel'],
    'Adam' : ['Amelia', 'Miguel', 'Sofia', 'Lucas'],
    'Miguel' : ['Amelia', 'Adam', 'Liam''Nathan'],
}

answer for shortest message from Jayden to Adam could be: 
['Jayden', 'Amelia', 'Adam']

Breakdown: graph is the appropriate DS
users are nodes, edges are the messages between users
input dictionary is representing the graph in adjacency list format.
is our graph directed or undirected? weighted or unweighted?

bfs or dfs? since we wanted the shortest path, BFS is the way to go

idea: let's do a breadth-first search of our graph starting from the 
sender and stopping when we find the recipient. Since we're using 
breadth-first search, we know that the first time we see the recipient, 
we'll have traveled to them along the shortest path.

'''
from collections import deque

def bfs(graph, start_node, end_node):
    nodes_to_visit = deque()
    nodes_to_visit.append(start_node)

    # keep track of what nodes we have already seen
    # so we don't process them twice
    nodes_already_seen = set([start_node])

    while len(nodes_to_visit) > 0:
        current_node = nodes_to_visit.popleft()

        # stop when we reach the end node
        if current_node == end_node:
            # found it
            break
        
        for neighbor in graph[current_node]:
            if neighbor not in nodes_already_seen:
                nodes_already_seen.add(neighbor)
                nodes_to_visit.append(neighbor)
'''
this looks on the right path but how to reconstruct the actual path taken?

we information do we need to store?
we'll need to somehow recover how we found each node. 
So, each time we find a new node, let's jot down what current_node was 
when we found it.
'''
from collections import deque

def bfs(graph, start_node, end_node):
    nodes_to_visit = deque()
    nodes_to_visit.append(start_node) 
    '''
    we could have done the above step like
    nodes_to_visit = deque([start_node]) # we need a list?
    nodes_to_visit = deque((start_node)) # this is tuple , may not be correct
    '''

    # keep track of what nodes we have already seen
    # so we don't process them twice
    nodes_already_seen = set([start_node])

    # keep track of how we got to each node
    # we'll use this to reconstruct the shortest path at the end
    how_we_reached_nodes = {start_node: None}

    while len(nodes_to_visit) > 0:
        current_node = nodes_to_visit.popleft()

        # stop when we reach the end node
        if current_node == end_node:
            # somehow reconstruct the path here
            return path
        
        for neighbor in graph[current_node]:
            if neighbor not in nodes_already_seen:
                nodes_already_seen.add(neighbor)
                nodes_to_visit.append(neighbor)
                # keep track of how we got to this node
                how_we_reached_nodes[neighbor] = current_node
'''
reconstructing path from end node
'''              
def reconstruct_path(how_we_reached_nodes, start_node, end_node):
    shortest_path = []

    # start from the end of the path and work backwards
    current_node = end_node

    while current_node:
        shortest_path.append(current_node)
        current_node = how_we_reached_nodes[current_node]

    return shortest_path
'''
One small thing though. Won't this return a path that has the 
recipient at the beginning?

so let's reverse it before returning it

shortest_path.reverse()
return shortest_path

are there any edge cases?
no grpah, start and end are the same nodes, unconnected graph

1. if there is no route, return None
2. what if either the sender or receiver aren't in our network? raise exception

these 2 looks fine, what about optimization?

we have two data structures- nodes _already_ seen and how_we_reached_nodes- 
that are updated in similar ways. In fact, every time we add a node to 
nodes_already_ seen, we also add it to how_we_reached_nodes. Do we need 
both of them?

we can reuse how_we_reached_nodes to save O(n) space
'''
from collections import deque

def reconstruct_path(previous_nodes, start_node, end_node):
    reversed_shortest_path = []

    # start from the end of the path and work backwards
    current_node = end_node
    while current_node:
        reversed_shortest_path.append(current_node)
        current_node = previous_nodes[current_node]

    # reverse our path to get the right order
    reversed_shortest_path.reverse() # flip it around, in place
    return reversed_shortest_path

def bsf_get_path(graph, start_node, end_node):
    if start_node not in graph:
        raise Exception('start node not in graph')
    if end_node not in graph:
        raise Exception('end node not in graph')
    
    nodes_to_visit = deque()
    nodes_to_visit.append(start_node)

    # keep track of how we got to each node
    # we'll use this to reconstruct the shortest path at the end
    # we'll also use this to keep track of which node we've already seen
    how_we_reached_nodes = {start_node: None}

    while len(nodes_to_visit) > 0:
        current_node = nodes_to_visit.popleft()

        # stop when we reach the end node
        if current_node == end_node:
            return reconstruct_path(how_we_reached_nodes, start_node, end_node)

        for neighbor in graph[current_node]:
            if neighbor not in how_we_reached_nodes:
                nodes_to_visit.append(neighbor)
                how_we_reached_nodes[neighbor] = current_node
    # if we get here, then we never found the end node
    # so there's no path from start_node to end_node
    return None
'''
Our solution has two main steps. First, we do a breadth-first search of the user network starting from the sender. Then, we use the results of our search to backtrack and find the shortest path.
How much work is a breadth-first search?
In the worst case, we'll go through the BFS loop once for every node in the graph, since we only ever add each node to nodes_to_visit once (we check how_we_reached_nodes to see if we've already added a node before). Each loop iteration involves a constant amount of work to dequeue the node and check if it's our end node. If we have n nodes, then this portion of the loop is O(N).
But there's more to each loop iteration: we also look at the current node's neighbors. Over all of the nodes in the graph, checking the neighbors is O(M), sincA it involves crossing each edge twice: once for each node at either end.
Putting this together, the complexity of the breadth-first search is ON + M).

What about backtracking to determine the shortest path? Handling each node in the path is O (1), and we could have at most N nodes in our shortest path. So, that's O(N) for building up the path.
Then, it's another ON) to reverse it. So, the total time complexity of our backtracking step is
O(N).
Putting these together, the time complexity of our entire algorithm is ON + M).
What about space complexity? The queue of nodes to visit, the mapping of nodes to previous nodes, and the final path ... they all store a constant amount of information per node. So, each data structure could take up to O(N) space if it stored information about all of our nodes. That means our overall space complexity is O(N).

Bonus:
1. In our solution, we assumed that if one user (Min) could transmit a message to another (Jayden), then Jayden would also be able to transmit a message to Min. Suppose this wasn't guaranteed-maybe Min's cell phone transmits over shorter distances than Jayden's. How would our graph change to represent this? Could we still use BFS?
Directed Graph (Asymmetric Transmission)
'''
# Represent graph as directed edges with transmission ranges
class User:
    def __init__(self, name, transmission_range):
        self.name = name
        self.transmission_range = transmission_range
        self.location = None  # (x, y) coordinates

def build_directed_network(users):
    """Build network based on transmission ranges."""
    network = {}
    for user1 in users:
        network[user1.name] = []
        for user2 in users:
            if user1 != user2:
                distance = calculate_distance(user1.location, user2.location)
                if distance <= user1.transmission_range:
                    network[user1.name].append(user2.name)
    return network

# BFS remains same, works with directed graphs

'''
Bonus:
2. What if we wanted to find the shortest path? Assume we're given a GPS location for each user. How could we incorporate the distance between users into our graph? How would our algorithm change?
Weighted Graph (GPS Distances)
'''
from heapq import heappush, heappop

def dijkstra_shortest_path(graph, start_node, end_node, locations):
    """Find shortest path considering GPS distances."""
    distances = {node: float('infinity') for node in graph}
    distances[start_node] = 0
    previous = {node: None for node in graph}
    pq = [(0, start_node)]
    
    while pq:
        current_distance, current_node = heappop(pq)
        
        if current_node == end_node:
            return reconstruct_path(previous, start_node, end_node)
            
        if current_distance > distances[current_node]:
            continue
            
        for neighbor in graph[current_node]:
            distance = calculate_gps_distance(
                locations[current_node],
                locations[neighbor]
            )
            new_distance = distances[current_node] + distance
            
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_node
                heappush(pq, (new_distance, neighbor))
    
    return None

def calculate_gps_distance(loc1, loc2):
    """Calculate distance between two GPS coordinates."""
    from math import radians, sin, cos, sqrt, atan2
    
    lat1, lon1 = map(radians, loc1)
    lat2, lon2 = map(radians, loc2)
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return 6371 * c  # Earth radius in km

'''
Bonus:
3. In our solution, we assumed that users never moved around. How could we extend our algorithm to handle the graph changing over time?
Dynamic Graph (Moving Users)
'''
from time import time
from collections import defaultdict

class DynamicNetwork:
    def __init__(self, update_interval=60):  # Update every 60 seconds
        self.users = {}  # {user_id: User}
        self.locations = defaultdict(list)  # {user_id: [(timestamp, location)]}
        self.update_interval = update_interval
        
    def update_user_location(self, user_id, location):
        """Update user's location with timestamp."""
        current_time = time()
        self.locations[user_id].append((current_time, location))
        self._cleanup_old_locations(user_id)
    
    def _cleanup_old_locations(self, user_id, max_age=3600):
        """Remove locations older than max_age seconds."""
        current_time = time()
        self.locations[user_id] = [
            (t, loc) for t, loc in self.locations[user_id]
            if current_time - t <= max_age
        ]
    
    def get_current_network(self):
        """Generate current network based on recent locations."""
        current_time = time()
        network = {}
        
        for user_id in self.users:
            network[user_id] = []
            user_location = self._get_latest_location(user_id)
            
            if user_location:
                for other_id in self.users:
                    if other_id != user_id:
                        other_location = self._get_latest_location(other_id)
                        if other_location:
                            if self._are_in_range(user_location, other_location):
                                network[user_id].append(other_id)
        
        return network
    
    def find_path(self, start_user, end_user):
        """Find path considering current locations."""
        current_network = self.get_current_network()
        return bsf_get_path(current_network, start_user, end_user)
    
    def _get_latest_location(self, user_id):
        """Get user's most recent location."""
        if user_id in self.locations and self.locations[user_id]:
            locations = sorted(self.locations[user_id], key=lambda x: x[0])
            if time() - locations[-1][0] <= self.update_interval:
                return locations[-1][1]
        return None
    
    def _are_in_range(self, loc1, loc2, max_range=1.0):  # 1km range
        """Check if two locations are within range."""
        return calculate_gps_distance(loc1, loc2) <= max_range
    

'''
what we learned:
The tricky part was backtracking to assemble the path we used to reach our end _node. In general, it's helpful to think of backtracking as two steps:
1. Figuring out what additional information we need to store in order to rebuild our path at the end (how_we_reached_nodes, in this case).
2. Figuring out how to reconstruct the path from that information.
And in this case, something interesting happened after we added how_we_reached_nodes-it made nodes_already_ seen redundant! So we were able to remove it. A good reminder to always look through your variables at the end and see if there are any you can cut out.

'''