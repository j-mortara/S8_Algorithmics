import random as rnd
import algo
import logging
import argparse


def analyze_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("max_vertices", help="the number max number of vertices in the graph", type=int)
    parser.add_argument("graph_number", help="the number of graph to generate and run", type=int)
    parser.add_argument("-d", "--debug", help="print debug logs, slows the program a lot, shouldn't run on big graph nor many examples", action="store_true")
    parser.add_argument("-r", "--recursive", help="run only the recursive version with different value for a and b", action="store_true")
    parser.add_argument("-e", "--export", help="export the generated graphs in the exports folder", action="store_true")
    return parser.parse_args()


def generate_erdos_renyi(max_vertices):
    v = rnd.randint(1, max_vertices)
    graph = {i: [] for i in range(1, v+1)}

    p = rnd.random()
    edges = [(i, j) for i in range(1, v+1) for j in range(1, i) if rnd.random() < p]

    for (i, j) in edges:
        graph[i].append(j)
        graph[j].append(i)

    return graph


def graph_to_file(graph, filename):
    with open(filename, 'w') as f:
        edges = [str(key) + " " + str(v) + "\n" for key, val in graph.items() for v in val if key < v]
        f.write(str(len(graph)) + " " + str(len(edges)) + "\n")
        f.writelines(edges)


def main():
    args = analyze_args()

    level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(format='[%(levelname)s] %(message)s', level=level)
    graphs = []
    logging.info(msg="Generating graphs...")
    for i in range(args.graph_number):
        g = generate_erdos_renyi(args.max_vertices)
        graph_to_file(g, "exports/graph_%d.txt" % i)
        graphs.append(g)
    logging.info(msg="Graph generation finished")

    version = algo.run_recursives if args.recursive else algo.run_all
    algo.run_case_suite_and_export(graphs, version)


if __name__ == '__main__':
    main()