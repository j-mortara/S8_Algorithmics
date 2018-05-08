import random as rnd
import algo

V = 8
N = 100


def generate_erdos_renyi(v):
    graph = {i: [] for i in range(1, v+1)}

    p = rnd.random()
    edges = [(i, j) for i in range(1, v+1) for j in range(1, i) if rnd.random() < p]

    for (i, j) in edges:
        graph[i].append(j)
        graph[j].append(i)

    return graph




def main():
    for _ in range(N):
        graph = generate_erdos_renyi(8)
        algo.run_all(graph)

if __name__ == '__main__':
    main()