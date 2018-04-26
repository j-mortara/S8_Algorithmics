import random

import math


# Original Karger algorithm
# A randomly selected edge is selected and contracted until two nodes remain.
# The min-cut value corresponds to the number of edges between those two nodes.
def karger(graph):
    # Prevents modifying the actual graph passed in parameter in case of several executions on the same graph
    graph = graph.copy()
    print("-----")
    while len(graph.items()) > 2:
        # random.sample returns a list of 1 element
        node_1, node_2 = random.sample(get_edges_list(graph), 1)[0]
        print(node_1, node_2)
        print("Contracting %d - %d" % (node_1, node_2))
        # Deleting node_2 and keeping the nodes it was linked to
        deleted_node_edges = graph.pop(node_2)
        for key, val in graph.items():
            # Every node previously linked to node_2 is now linked to node_1
            if key != node_1:
                graph[key] = [i if i != node_2 else node_1 for i in val]
            # Links for node_1 are updated from the links of node_2
            else:
                graph[key] = [i for i in val if i != node_2] + [i for i in deleted_node_edges if i != node_1]
        print(graph)
    return graph


# Improved Karger algorithm
# Runs two times a recursive algorithm, then returns the minimum min-cut value found
def karger_improved(graph, nb_contract=math.sqrt(2), nb_recur=2):
    return min([karger_recursive(graph.copy(), nb_contract) for _ in range(nb_recur)], key=cut_value)


# Instead of contracting the graph until only two nodes remain, the contraction is done until n/nb_contract nodes
# remain, then a recursive call is done on the resulting graph.
def karger_recursive(graph, nb_contract):
    n = len(graph.items())
    if len(graph.items()) == 2:
        return graph
    else:
        print("-----")
        while len(graph.items()) > n / nb_contract:
            node_1, node_1_list = random.choice(list(graph.items()))
            node_2 = random.choice(node_1_list)
            print("Contracting %d - %d" % (node_1, node_2))
            # Deleting node_2 and keeping the nodes it was linked to
            deleted_node_edges = graph.pop(node_2)
            for key, val in graph.items():
                # Everything linked to node_2 is now linked to node_1
                if key != node_1:
                    graph[key] = [i if i != node_2 else node_1 for i in val]
                # Links for node_1 are updated from the links of node_2
                else:
                    graph[key] = [i for i in val if i != node_2] + [i for i in deleted_node_edges if i != node_1]
            print(graph)
        return karger_recursive(graph, nb_contract)


# Returns the number of edges between the two remaining nodes.
# This value is found by grabbing the number of edges of one of those two nodes, here the first one.
# Example of cut : {1: [2, 2, 2], 2: [1, 1, 1]}
def cut_value(graph):
    return len(graph[list(graph.keys())[0]])


# Returns a list containing the graph edges
# For each couple of vertices a and b, the edge represented with (a,b) and (b,a) are the same.
# We decide to represent an edge by a tuple (a,b) with "a" being the node of smallest index.
# So if a < b, we add (a,b). Otherwise, we add (b,a)
# A set is used to be sure that each edge is added only once.
def get_edges_list(graph):
    edges_set = set()
    for key, val in graph.items():
        for n in val:
            edges_set.add((key, n) if key < n else (n, key))
    return edges_set


if __name__ == '__main__':
    # A graph can be represented with a dictionary
    # Key : node
    # Value : list of the nodes linked to the node
    input_graph = {1: [2, 3, 4], 2: [1, 4], 3: [1], 4: [1, 2]}
    input_graph2 = {1: [2, 3, 4, 6], 2: [1, 4, 5, 7], 3: [1, 6, 7], 4: [1, 2, 5, 6], 5: [2, 4], 6: [1, 3, 4], 7: [2, 3]}
    example_cut = {1: [2, 2, 2], 2: [1, 1, 1]}
    k1 = karger(input_graph2)
    print("Karger : " + str(k1))
    k2 = karger_improved(input_graph2)
    print("Recursive Karger : " + str(k2))
