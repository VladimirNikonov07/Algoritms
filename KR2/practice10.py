from itertools import combinations


def graph(vertices, edges):
    adj = {u: set() for u in vertices}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def greedy(adj):
    colors = {}
    for v in sorted(adj):
        used = {colors[u] for u in adj[v] if u in colors}
        c = 1
        while c in used:
            c += 1
        colors[v] = c
    return colors


def welsh_powell(adj):
    order = sorted(adj, key=lambda v: (-len(adj[v]), v))
    colors = {}
    color = 0
    while len(colors) < len(adj):
        color += 1
        for v in order:
            if v not in colors and all(colors.get(u) != color for u in adj[v]):
                colors[v] = color
    return colors


def cliques(adj):
    result = []

    def visit(chosen, possible, excluded):
        # Когда оба множества пусты, клику больше нельзя расширить.
        if not possible and not excluded:
            result.append(tuple(sorted(chosen)))
        for v in sorted(possible):
            visit(chosen | {v}, possible & adj[v], excluded & adj[v])
            possible.remove(v)
            excluded.add(v)

    visit(set(), set(adj), set())
    return sorted(result)


def exact(adj):
    order = sorted(adj, key=lambda v: (-len(adj[v]), v))
    colors = {}

    def assign(i, limit):
        if i == len(order):
            return True
        v = order[i]
        for c in range(1, limit + 1):
            if all(colors.get(u) != c for u in adj[v]):
                colors[v] = c
                if assign(i + 1, limit):
                    return True
                del colors[v]
        return False

    for limit in range(1, len(adj) + 1):
        if assign(0, limit):
            return limit, colors.copy()


def task1():
    adj = graph("ABCDEFGH", "AB AC AD AE BC BF CD CF CG DE DG EH FG FH GH".split())
    for name, method in [('Жадная', greedy), ('Вельш–Пауэлл', welsh_powell)]:
        colors = method(adj)
        print(name, sorted(colors.items()), "цветов:", max(colors.values()))
    number, colors = exact(adj)
    print("Хроматическое число:", number, "| пример:", sorted(colors.items()))


def task2():
    adj = graph("ABCDEFGH", "AB AC AD BC BD CD CE DF EF EG FG FH GH".split())
    maximal = cliques(adj)
    largest = max(maximal, key=len)
    missing = [(u,v) for u,v in combinations(adj, 2) if v not in adj[u]]
    complement = graph(adj, missing)
    print("Максимальные клики:", [''.join(c) for c in maximal])
    print("Наибольшая:", ''.join(largest), "| χ ≥", len(largest))
    print("Рёбра дополнения:", ' '.join(u+v for u,v in missing))
    print("Максимальные независимые:", [''.join(c) for c in cliques(complement)])


def task3():
    vertices = ['M1','M2','M3','P1','P2','P3']
    pairs = ['M1-M2','M1-M3','M1-P1','M2-M3','M2-P2','M3-P1',
             'M3-P2','M3-P3','P1-P2','P1-P3','P2-P3']
    edges = [p.split('-') for p in pairs]
    adj = graph(vertices, edges)
    colors = welsh_powell(adj)
    number, _ = exact(adj)
    print("Минимум слотов:", number)
    print("Клика:", max(cliques(adj), key=len))
    for slot in range(1, max(colors.values()) + 1):
        print("Слот", slot, [v for v in vertices if colors[v] == slot])
    print("Все занятия распределены:", set(colors) == set(vertices))
    print("Все конфликты учтены:", all(colors[u] != colors[v] for u,v in edges))


if __name__ == '__main__':
    for number, task in enumerate([task1, task2, task3], 1):
        print(f"Задание {number}")
        task()
