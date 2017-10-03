# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.
# Your answers will look like one of the two below:
# ANSWER1 = True
# ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

# Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.


def bfs(graph, start, goal):
    queue = [[start]]
    while len(queue) > 0:
        if queue[0][-1] == goal:
            break
        path = queue.pop(0)
        last_node = path[-1]
        neighbors = graph.get_connected_nodes(last_node)
        new_paths = [path + [neighbor]
                     for neighbor in neighbors if neighbor not in path]
        queue += new_paths
    if queue:
        return queue[0]
    else:
        return []


def dfs(graph, start, goal):
    queue = [[start]]
    while len(queue) > 0:
        if queue[0][-1] == goal:
            break
        path = queue.pop(0)
        last_node = path[-1]
        neighbors = graph.get_connected_nodes(last_node)
        new_paths = [path + [neighbor]
                     for neighbor in neighbors if neighbor not in path]
        queue = new_paths + queue
    if queue:
        return queue[0]
    else:
        return []


# Now we're going to add some heuristics into the search.
# Remember that hill-climbing is a modified version of depth-first search.
# Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    queue = [[start]]
    while len(queue) > 0:
        if queue[0][-1] == goal:
            break
        path = queue.pop(0)
        last_node = path[-1]
        neighbors = graph.get_connected_nodes(last_node)
        new_paths = [path + [neighbor]
                     for neighbor in neighbors if neighbor not in path]

        new_paths.sort(key=lambda x: graph.get_heuristic(x[-1], goal))
        queue = new_paths + queue
    if queue:
        return queue[0]
    else:
        return []


# Now we're going to implement beam search, a variation on BFS
# that caps the amount of memory used to store paths.  Remember,
# we maintain only k candidate paths of length n in our agenda at any time.
# The k top candidates are to be determined using the
# graph get_heuristic function, with lower values being better values.


def beam_search(graph, start, goal, beam_width):
    queue = [[start]]
    while len(queue) > 0:
        if queue[0][-1] == goal:
            break
        path = queue.pop(0)
        last_node = path[-1]
        neighbors = graph.get_connected_nodes(last_node)
        new_paths = [path + [neighbor]
                     for neighbor in neighbors if neighbor not in path]
        queue += new_paths
        if len(queue) and (not len(path) == len(queue[0])):
            queue.sort(key=lambda x: graph.get_heuristic(x[-1], goal))
            queue = queue[:beam_width]
    if queue:
        return queue[0]
    else:
        return []

# Now we're going to try optimal search.  The previous searches haven't
# used edge distances in the calculation.

# This function takes in a graph and a list of node names, and returns
# the sum of edge lengths along the path -- the total distance in the path.


def path_length(graph, node_names):
    length = 0
    for i in xrange(len(node_names)):
        if i == len(node_names) - 1:
            continue
        edge = graph.get_edge(node_names[i], node_names[i + 1])
        length += edge.length
    return length


def branch_and_bound(graph, start, goal):
    queue = [[start]]
    while len(queue) > 0:
        if queue[0][-1] == goal:
            break
        path = queue.pop(0)
        last_node = path[-1]
        neighbors = graph.get_connected_nodes(last_node)
        new_paths = [path + [neighbor]
                     for neighbor in neighbors if neighbor not in path]
        queue = new_paths + queue
        queue.sort(key=lambda x: path_length(graph, x))
    if queue:
        return queue[0]
    else:
        return []


def a_star(graph, start, goal):
    queue = [[start]]
    extended = []
    while len(queue) > 0:
        if queue[0][-1] == goal:
            break
        path = queue.pop(0)
        last_node = path[-1]
        extended.append(last_node)
        neighbors = graph.get_connected_nodes(last_node)
        new_paths = [path + [neighbor]
                     for neighbor in neighbors if (neighbor not in path) and (neighbor not in extended)]
        queue = new_paths + queue
        queue.sort(key=lambda x: path_length(graph, x) +
                   graph.get_heuristic(x[-1], goal))
    if queue:
        return queue[0]
    else:
        return []


# It's useful to determine if a graph has a consistent and admissible
# heuristic.  You've seen graphs with heuristics that are
# admissible, but not consistent.  Have you seen any graphs that are
# consistent, but not admissible?
# You've learned that in order for the
# heuristic to be admissible, the heuristic value for every node in a graph must be less than or equal to the
# distance of the shortest path from the goal to that node.
# #In order for a heuristic to be consistent, for each
# edge in the graph, the edge length must be greater than or equal to the absolute value of the difference
# between the two heuristic values of its nodes.

def is_admissible(graph, goal):
    for node in graph.nodes:
        est = graph.get_heuristic(node, goal)
        opt_path = a_star(graph, node, goal)
        opt_path_length = path_length(graph, opt_path)
        if est > opt_path_length:
            return False
    return True


def is_consistent(graph, goal):
    for edge in graph.edges:
        est_1 = graph.get_heuristic(edge.node1, goal)
        est_2 = graph.get_heuristic(edge.node2, goal)
        if edge.length < abs(est_1 - est_2):
            return False
    return True


HOW_MANY_HOURS_THIS_PSET_TOOK = '2'
WHAT_I_FOUND_INTERESTING = 'Branch And Bound'
WHAT_I_FOUND_BORING = 'The repetition?'
