import random
import time
import math
import csv
import logging
import time

last_update = 0

# Original Karger algorithm
# A randomly selected edge is selected and contracted until two nodes remain.
# The min-cut value corresponds to the number of edges between those two nodes.
def karger(graph):
    # Prevents modifying the actual graph passed in parameter in case of several executions on the same graph
    graph = graph.copy()
    logging.debug("-----")
    while len(graph.items()) > 2:
        # random.sample returns a list of 1 element
        edge_list = get_edges_list(graph)
        if len(edge_list) < 1:
            return graph
        node_1, node_2 = random.sample(edge_list, 1)[0]
        logging.debug("Contracting %d - %d" % (node_1, node_2))
        # Deleting node_2 and keeping the nodes it was linked to
        deleted_node_edges = graph.pop(node_2)
        for key, val in graph.items():
            # Every node previously linked to node_2 is now linked to node_1
            if key != node_1:
                graph[key] = [i if i != node_2 else node_1 for i in val]
            # Links for node_1 are updated from the links of node_2
            else:
                graph[key] = [i for i in val if i != node_2] + [i for i in deleted_node_edges if i != node_1]
        logging.debug(graph)
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
        logging.debug("-----")
        while len(graph.items()) > n / nb_contract:
            edge_list = get_edges_list(graph)
            if len(edge_list) < 1:
                return graph
            node_1, node_2 = random.sample(edge_list, 1)[0]
            logging.debug("Contracting %d - %d" % (node_1, node_2))
            # Deleting node_2 and keeping the nodes it was linked to
            deleted_node_edges = graph.pop(node_2)
            for key, val in graph.items():
                # Everything linked to node_2 is now linked to node_1
                if key != node_1:
                    graph[key] = [i if i != node_2 else node_1 for i in val]
                # Links for node_1 are updated from the links of node_2
                else:
                    graph[key] = [i for i in val if i != node_2] + [i for i in deleted_node_edges if i != node_1]
            logging.debug(graph)
        return karger_recursive(graph, nb_contract)


def stoer_wagner(graph):
    # print len(graph)
    while len(graph) > 2:
        # TODO: use importance sampling
        start_index, start_val = random.choice(list(graph.items()))
        finish = random.choice(start_val)

        # print start_index, finish
        # # Adding the edges from the absorbed node:
        for edge in graph[finish]:
            if edge != start_index:  # this stops us from making a self-loop
                graph[start_index].append(edge)

        # # Deleting the references to the absorbed node and changing them to the source node:
        for edge1 in graph[finish]:
            graph[edge1].remove(finish)
            if edge1 != start_index:  # this stops us from re-adding all the edges in start_index.
                graph[edge1].append(start_index)
        del graph[finish]

    # # Calculating and recording the mincut
    mincut = cut_value(graph)
    print(mincut)
    # print graph
    return graph


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


def run_all(graph):
    return {'karger': karger(graph), 'karger_improved': karger_improved(graph), 'karger_recursive': karger_improved(graph, 2, 3)}


def run_case_suite_and_export(graph_list):
    # TODO interesting metrics
    c_example = "Exemple"
    c_algo = "Algorithme"
    c_min_cut = "Coupe min"
    columns = [c_example, c_algo, c_min_cut]
    filename = str(int(time.time() * 1000)) + '_analytics.csv'
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()

        logging.info("Starting min-cut computations...")
        last_update = time.time()
        total = len(graph_list)
        for i, graph in enumerate(graph_list):
            for algo, res in run_all(graph).items():
                # Extract min cut result, throw an exception if the result isn't coherent
                min_cut = -1
                for _, value in res.items():
                    if min_cut == -1:
                        min_cut = len(value)
                    else:
                        if min_cut != len(value):
                            raise RuntimeError('Result isn\'t coherent.')
                # Write CSV
                row = {}
                row[c_example] = i + 1
                row[c_algo] = algo
                row[c_min_cut] = min_cut
                writer.writerow(row)

            if (time.time() - last_update >= 2):
                logging.info("%d / %d computed (%d%%)" % (i, total, int(i/total*100)))
                last_update = time.time()
    logging.info("Computations finished, analytics stored in '%s'" % filename)


if __name__ == '__main__':
    # A graph can be represented with a dictionary
    # Key : node
    # Value : list of the nodes linked to the node
    input_graph = {1: [2, 3, 4], 2: [1, 4], 3: [1], 4: [1, 2]}
    input_graph2 = {1: [2, 3, 4, 6], 2: [1, 4, 5, 7], 3: [1, 6, 7], 4: [1, 2, 5, 6], 5: [2, 4], 6: [1, 3, 4], 7: [2, 3]}
    example_cut = {1: [2, 2, 2], 2: [1, 1, 1]}
    logging.debug("Karger :")
    k1 = karger(input_graph2)
    logging.debug("Karger result : " + str(k1), end="\n\n")
    logging.debug("Recursive Karger :")
    k2 = karger_improved(input_graph2)
    logging.debug("Recursive Karger result : " + str(k2))
