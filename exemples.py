import glob
import argparse
import algo
import logging

def analyze_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="print debug logs, slows the program a lot, shouldn't run on big graph nor many examples", action="store_true")
    parser.add_argument("-r", "--recursive", help="run only the recursive version with different value for a and b", action="store_true")
    return parser.parse_args()


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


def main():
    args = analyze_args()

    level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(format='[%(levelname)s] %(message)s', level=level)
    graphs = []
    logging.info(msg="Parsing examples...")
    for f in glob.glob("exemples/*"):
        graphs.append(file_to_graph(f))
    logging.info(msg="Example parsing finished")

    version = algo.run_recursives if args.recursive else algo.run_all
    algo.run_case_suite_and_export(graphs, version)


if __name__ == '__main__':
    main()