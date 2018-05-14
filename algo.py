import random
import math
import csv
import logging
import time

contractions = 0

# Values for the recursive a and b research
# To modify them, please go to run_recursives function
min_a = 0
max_a = 0
step_a = 0.0
min_b = 0
max_b = 0
step_b = 0

# Original Karger algorithm
# A randomly selected edge is selected and contracted until two nodes remain.
# The min-cut value corresponds to the number of edges between those two nodes.
def karger(graph):
    global contractions
    # Prevents modifying the actual graph passed in parameter in case of several executions on the same graph
    graph = graph.copy()
    while len(graph.items()) > 2:
        # random.sample returns a list of 1 element
        edge_list = get_edges_list(graph)
        if len(edge_list) < 1:
            return graph
        node_1, node_2 = random.sample(edge_list, 1)[0]
        contractions += 1
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
    return graph


# Improved Karger algorithm
# Runs two times a recursive algorithm, then returns the minimum min-cut value found
def karger_improved(graph, nb_contract=math.sqrt(2), nb_recur=2):
    res = []
    for _ in range(nb_recur):
        res.append(karger_recursive(graph.copy(), nb_contract))
    if len(res) == 0:
        return {}
    return min(res, key=cut_value)


# Instead of contracting the graph until only two nodes remain, the contraction is done until n/nb_contract nodes
# remain, then a recursive call is done on the resulting graph.
def karger_recursive(graph, nb_contract):
    global contractions
    n = len(graph.items())
    if len(graph.items()) == 2:
        return graph
    else:
        while len(graph.items()) > n / nb_contract:
            edge_list = get_edges_list(graph)
            if len(edge_list) < 1:
                return graph
            node_1, node_2 = random.sample(edge_list, 1)[0]
            contractions += 1
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
    global contractions
    res = {}
    contractions = 0
    res['karger'] = karger(graph), contractions
    contractions = 0
    res['karger_improved'] = karger_improved(graph), contractions
    contractions = 0
    n = len(graph)
    res['karger_recursive'] = karger_improved(graph, 3.5, (n**2)//2), contractions

    return res


def run_recursives(graph):
    global contractions, min_a, max_a, step_a, min_b, max_b, step_b

    n = len(graph)
    min_a = 1
    max_a = 5
    # maximum precision is 1e-1
    step_a = 0.1
    min_b = n
    max_b = n**2
    step_b = n

    res = {}
    for a in [int((x/10 + step_a) * 10) / 10 for x in range(int(min_a*10), int(max_a*10))]:
    # for b in range(min_b, max_b + 1, step_b):
        contractions = 0
        logging.info("Testing with a=%.1f and b=%d" % (a, int(max_b/2)))
        res['karger_recursive_a%.1f_b%d' % (a, int(max_b/2))] = karger_improved(graph, a, int(max_b/2)), contractions
    #res['karger_recursive_a3.5'] = karger_improved(graph, 3.5, int(max_b/2)), contractions
    #res['karger_recursive_an^0.75'] = karger_improved(graph, n ** 0.75, int(max_b/2)), contractions
    return res


def run_case_suite_and_export(graph_list, run_function=run_all):
    # TODO interesting metrics
    c_example = "Exemple"
    c_algo = "Algorithme"
    c_edges = "Nombre d'arêtes"
    c_min_cut = "Coupe min"
    c_contractions = "Nombre de contractions"
    columns = [c_example, c_algo, c_edges, c_min_cut, c_contractions]
    filename = str(int(time.time() * 1000)) + '_analytics.csv'
    with open(filename, 'w', encoding="UTF-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()

        logging.info("Starting min-cut computations...")
        last_update = time.time()
        total = len(graph_list)
        for i, graph in enumerate(graph_list):
            edges_number = len(get_edges_list(graph))
            for algo, (res, contractions) in run_function(graph).items():
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
                row[c_edges] = edges_number
                row[c_min_cut] = min_cut
                row[c_contractions] = contractions
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
