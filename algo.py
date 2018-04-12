import random

import math


# Original Karger algorithm
# A randomly selected vertex is selected and contracted until two nodes remain.
# The min-cut value corresponds to the number of vertices between those two nodes.
def karger(graph):
    # Prevents modifying the actual graph passed in parameter in case of several executions on the same graph
    graph = graph.copy()
    print("-----")
    while len(graph.items()) > 2:
        node_1, node_1_list = random.choice(list(graph.items()))
        node_2 = random.choice(node_1_list)
        print("Contracting %d - %d" % (node_1, node_2))
        # Deleting node_2 and keeping the nodes it was linked to
        deleted_node_vertices = graph.pop(node_2)
        for key, val in graph.items():
            # Everything linked to node_2 is now linked to node_1
            if key != node_1:
                graph[key] = [i if i != node_2 else node_1 for i in val]
            # Links for node_1 are updated from the links of node_2
            else:
                graph[key] = [i for i in val if i != node_2] + [i for i in deleted_node_vertices if i != node_1]
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
            deleted_node_vertices = graph.pop(node_2)
            for key, val in graph.items():
                # Everything linked to node_2 is now linked to node_1
                if key != node_1:
                    graph[key] = [i if i != node_2 else node_1 for i in val]
                # Links for node_1 are updated from the links of node_2
                else:
                    graph[key] = [i for i in val if i != node_2] + [i for i in deleted_node_vertices if i != node_1]
            print(graph)
        return karger_recursive(graph, nb_contract)


# Returns the number of vertices between the two remaining nodes.
# This value is found by grabbing the number of vertices of one of those two nodes, here the first one.
# Example of cut : {1: [2, 2, 2], 2: [1, 1, 1]}
def cut_value(graph):
    return len(graph[list(graph.keys())[0]])


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
