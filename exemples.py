def file_to_graph(filename):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    lines = [sorted([int(j) for j in i.split()]) for i in lines]
    graph = {}
    for i, j in lines[1:]:
        add_edge_to_graph(graph, i, j)
        add_edge_to_graph(graph, j, i)
    return graph


def add_edge_to_graph(graph, i, j):
    if i not in graph:
        graph[i] = []
    graph[i].append(j)
