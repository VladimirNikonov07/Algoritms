from collections import Counter, defaultdict
from heapq import heappush, heappop


def parse(data):
    return [(e[0], e[1], int(e[2:])) for e in data.split()]


def kruskal(edges):
    parent = {v: v for u, v, w in edges for v in (u, v)}
    rank = dict.fromkeys(parent, 0)

    def root(v):
        while v != parent[v]:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    tree = []
    for u, v, w in sorted(edges, key=lambda edge: edge[2]):
        a, b = root(u), root(v)
        if a == b:
            continue
        if rank[a] < rank[b]:
            a, b = b, a
        parent[b] = a
        if rank[a] == rank[b]:
            rank[a] += 1
        tree.append((u, v, w))
    return tree


def prim(edges, start):
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((w, u, v))
        graph[v].append((w, v, u))
    tree, visited, queue = [], {start}, []
    for edge in graph[start]:
        heappush(queue, edge)
    while queue:
        w, u, v = heappop(queue)
        if v in visited:
            continue
        visited.add(v)
        tree.append((u, v, w))
        for edge in graph[v]:
            if edge[2] not in visited:
                heappush(queue, edge)
    return tree


def total(tree):
    return sum(w for u, v, w in tree)


def show(tree):
    for u, v, w in tree:
        print(f"  {u} — {v}: {w}")
    print("Сумма:", total(tree))


def cut(edges, tree, removed):
    # После удаления ребра дерева достижимые из его начала образуют разрез.
    side = {removed[0]}
    for _ in tree:
        for edge in tree:
            u, v, _ = edge
            if edge != removed and (u in side or v in side):
                side.update([u, v])
    minimum = min(w for u, v, w in edges if (u in side) != (v in side))
    print(removed, "сторона", ''.join(sorted(side)), "минимум", minimum)
    assert minimum == removed[2]


def compare(edges, start):
    tree = kruskal(edges)
    other = prim(edges, start)
    print("Краскал:")
    show(tree)
    print("Прим:")
    show(other)
    assert total(tree) == total(other)
    return tree


def task1():
    # В пересечении BF и DE читается общая метка 5.
    edges = parse("AB6 AC4 AD8 BC2 BE7 BF5 CD3 DE5 DF5 DG6 EF4 EH3 FG2 FH8 GH5")
    tree = compare(edges, 'A')
    cut(edges, tree, tree[0])


def task2():
    cities = ['Москва', 'Петербург', 'Нижний Новгород', 'Казань', 'Самара',
              'Уфа', 'Екатеринбург', 'Тюмень', 'Волгоград', 'Ростов', 'Краснодар']
    roads = [(0,1,650), (1,2,1200), (0,2,400), (2,3,400), (0,3,800),
             (3,4,450), (3,5,500), (4,5,450), (5,6,550), (6,7,350),
             (0,9,1100), (4,9,900), (4,8,850), (8,9,400), (9,10,250)]
    edges = [(cities[u], cities[v], w) for u, v, w in roads]
    tree = kruskal(edges)
    show(tree)
    degrees = Counter(x for u, v, _ in tree for x in (u, v))
    print("Центры:", [v for v in degrees if degrees[v] == max(degrees.values())])
    updated = kruskal(edges + [('Москва', 'Казань', 500)])
    print("С дорогой 500 км:", total(updated), "км. Те же рёбра:", updated == tree)


def task3():
    # У пересекающихся 26 и 35 видна одна метка 2. На рисунке 15 линий.
    edges = parse("127 134 149 236 253 262 345 352 475 467 564 586 673 685 782")
    tree = compare(edges, '1')
    for edge in tree:
        cut(edges, tree, edge)
    print("V = 8, E =", len(edges), "| Краскал O(E log E), Прим O(E log V)")


if __name__ == '__main__':
    for number, task in enumerate([task1, task2, task3], 1):
        print(f"Задание {number}")
        task()

