from heapq import heappop, heappush
from itertools import count
from math import hypot, inf


def graph_from(data):
    graph = {}
    for edge in data.split():
        u, v = edge[:2]
        weight = int(edge[2:])
        graph.setdefault(u, []).append((v, weight))
        graph.setdefault(v, []).append((u, weight))
    return graph


def search(graph, start, goal, heuristic):
    order = count()
    queue = [(heuristic(start), next(order), 0, start)]
    distance = {start: 0}
    previous = {}
    visited = []
    while queue:
        _, _, cost, u = heappop(queue)
        if cost != distance[u]:
            continue
        visited.append(u)
        if u == goal:
            path = [goal]
            while path[-1] != start:
                path.append(previous[path[-1]])
            return path[::-1], cost, visited
        for v, step in graph[u]:
            new_cost = cost + step
            if new_cost < distance.get(v, inf):
                previous[v] = u
                distance[v] = new_cost
                # Счётчик сохраняет порядок вставки при равных оценках.
                heappush(queue, (new_cost + heuristic(v), next(order),
                                 new_cost, v))
    return [], inf, visited


def compare(graph, start, goal, methods):
    for title, h in methods:
        path, cost, visited = search(graph, start, goal, h)
        print(title, "| длина:", cost, "| исследовано:", len(visited))
        print("Путь:", " ".join(map(str, path)))
        if isinstance(start, str):
            print("Порядок:", " ".join(visited))


def task1():
    graph = graph_from("AB3 AC5 BD4 BE7 CD2 CF6 DE3 DG8 FG4 EH5 GH2 HT6 GT7")
    coords = dict(A=(0,3), B=(1,1), C=(1,5), D=(2,3), E=(2,0),
                  F=(2,6), G=(3,4), H=(3,0), T=(4,2))
    # Масштаб 1/2 обеспечивает стоимость шага не ниже его L1-длины.
    def h(v):
        x, y = coords[v]
        return (abs(x-4) + abs(y-2)) / 2
    assert all(h(v) <= search(graph, v, 'T', lambda _: 0)[1] for v in graph)
    compare(graph, 'A', 'T', [('A*', h), ('Дейкстра', lambda _: 0)])


def task2():
    maze = ['S..#....', '.#.#.##.', '.#....#.', '.####.#.',
            '....#...', '###.###.', '........', '.#####.G']
    graph = {}
    for r, row in enumerate(maze):
        for c, cell in enumerate(row):
            if cell == '#':
                continue
            graph[r,c] = []
            for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
                i, j = r + dr, c + dc
                if 0 <= i < 8 and 0 <= j < 8 and maze[i][j] != '#':
                    graph[r,c].append(((i,j), 1))
    compare(graph, (0,0), (7,7), [
        ('Манхэттен', lambda v: abs(7-v[0]) + abs(7-v[1])),
        ('Евклид', lambda v: hypot(7-v[0], 7-v[1])),
        ('Дейкстра', lambda _: 0)])


def task3():
    graph = graph_from("AB2 AC4 BD5 CD1 CE7 DF3 EF2 EG6 FH4 GH3 HT5")
    h = dict(A=8, B=7, C=6, D=5, E=4, F=3, G=3, H=2, T=0)
    for v in sorted(graph):
        exact = search(graph, 'T', v, lambda _: 0)[1]
        print(v, "h =", h[v], "d =", exact, "допустима:", h[v] <= exact)
    compare(graph, 'A', 'T', [('A*', h.get), ('Дейкстра', lambda _: 0)])


if __name__ == '__main__':
    for number, task in enumerate([task1, task2, task3], 1):
        print(f"Задание {number}")
        task()
