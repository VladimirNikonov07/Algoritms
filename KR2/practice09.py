from collections import Counter, defaultdict
from itertools import combinations
from math import inf


def graph(edges):
    result = defaultdict(list)
    for u, v in edges:
        result[u].append(v)
        result[v].append(u)
    return result


def reached(adj, start):
    seen, stack = {start}, [start]
    while stack:
        for v in adj[stack.pop()]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return seen


def fleury(edges):
    adj = graph(edges)
    odd = sorted(v for v in adj if len(adj[v]) % 2)
    if len(odd) not in (0, 2) or len(reached(adj, edges[0][0])) != len(adj):
        return []
    u = odd[0] if odd else edges[0][0]
    path = [u]
    while adj[u]:
        # Временно удаляем один экземпляр ребра и проверяем достижимость.
        for v in sorted(adj[u]):
            single = len(adj[u]) == 1
            adj[u].remove(v)
            adj[v].remove(u)
            if single or v in reached(adj, u):
                break
            adj[u].append(v)
            adj[v].append(u)
        u = v
        path.append(u)
    traversed = Counter(tuple(sorted(e)) for e in zip(path, path[1:]))
    assert traversed == Counter(tuple(sorted(e)) for e in edges)
    return path


def task1():
    edges = [tuple(e) for e in "AB AC AD BC BE CD CE CF DF EF EG FG".split()]
    adj = graph(edges)
    print("Степени:", {v: len(adj[v]) for v in sorted(adj)})
    odd = sorted(v for v in adj if len(adj[v]) % 2)
    print("Нечётные вершины:", odd)
    print("Маршрут Флёри:", fleury(edges) or "невозможен")


def matching(vertices, distance):
    if not vertices:
        return 0, []
    u = vertices[0]
    choices = []
    for v in vertices[1:]:
        rest = [x for x in vertices if x not in (u, v)]
        cost, pairs = matching(rest, distance)
        choices.append((distance[u,v] + cost, [(u,v)] + pairs))
    return min(choices)


def task2():
    data = "AB6 AC3 AD8 BD5 BE4 CD2 CF7 DE3 DF6 EF4 EG5 FG2"
    weights = {(e[0], e[1]): int(e[2:]) for e in data.split()}
    edges = list(weights)
    adj = graph(edges)
    odd = sorted(v for v in adj if len(adj[v]) % 2)
    distance = {(u,v): 0 if u == v else inf for u in adj for v in adj}
    following = {}
    for (u,v), w in weights.items():
        distance[u,v] = distance[v,u] = w
        following[u,v], following[v,u] = v, u
    for k in adj:
        for u in adj:
            for v in adj:
                via = distance[u,k] + distance[k,v]
                if via < distance[u,v]:
                    distance[u,v] = via
                    following[u,v] = following[u,k]
    print("Нечётные:", odd)
    print("Расстояния:", {u+v: distance[u,v] for u,v in combinations(odd, 2)})
    extra, pairs = matching(odd, distance)
    print("Паросочетание:", pairs, "| добавка:", extra)
    for u, v in pairs:
        while u != v:
            w = following[u,v]
            edges.append((u,w))
            u = w
    route = fleury(edges)
    print("Цикл:", " -> ".join(route))
    actual = sum(weights[tuple(sorted(e))] for e in zip(route, route[1:]))
    assert actual == sum(weights.values()) + extra
    print("Длина:", sum(weights.values()), "+", extra, "=", actual)


def task3():
    edges = [tuple(e) for e in "AB AC AF BC BD CD CE DE DF EF".split()]
    adj = graph(edges)

    def extend(path):
        if len(path) == len(adj):
            return path + [path[0]] if path[0] in adj[path[-1]] else []
        for v in sorted(adj[path[-1]]):
            if v not in path:
                solution = extend(path + [v])
                if solution:
                    return solution
        return []

    print("Цикл:", " -> ".join(extend(['A'])))
    print("Степени:", {v: len(adj[v]) for v in sorted(adj)})
    print("Условие Дирака:", min(map(len, adj.values())) >= len(adj)/2)
    print("При старте в A до (6-1)!/2 = 60 циклов без учёта ориентации.")


if __name__ == '__main__':
    for number, task in enumerate([task1, task2, task3], 1):
        print(f"Задание {number}")
        task()
