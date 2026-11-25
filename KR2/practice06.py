from math import inf, log, prod


def bellman(vertices, edges, start):
    distance = dict.fromkeys(vertices, inf)
    distance[start] = 0
    previous = {}
    changed = None
    for _ in vertices:
        changed = None
        for u, v, weight in edges:
            if distance[u] + weight < distance[v] - 1e-12:
                distance[v] = distance[u] + weight
                previous[v] = u
                changed = v
        if changed is None:
            break
    # Изменение на последнем проходе указывает на достижимый цикл.
    cycle = []
    if changed is not None:
        for _ in vertices:
            changed = previous[changed]
        cycle = [changed]
        vertex = previous[changed]
        while vertex != changed:
            cycle.append(vertex)
            vertex = previous[vertex]
        cycle.append(changed)
        cycle.reverse()
    return distance, previous, cycle


def floyd(matrix):
    result = [row[:] for row in matrix]
    for k in range(len(result)):
        for i in range(len(result)):
            for j in range(len(result)):
                via = result[i][k] + result[k][j]
                result[i][j] = min(result[i][j], via)
    return result


def show_matrix(matrix):
    for row in matrix:
        print(" ".join(f"{x:4}" for x in row))


def task1():
    edges = [('S','A',4), ('S','B',3), ('A','B',-2), ('A','C',7),
             ('B','C',5), ('B','D',8), ('C','D',-1), ('C','T',6),
             ('D','T',3)]
    distances, previous, cycle = bellman("SABCDT", edges, 'S')
    path = ['T']
    while path[-1] != 'S':
        path.append(previous[path[-1]])
    print("Расстояния:", distances)
    print("Путь:", " -> ".join(reversed(path)))
    print("Отрицательный цикл:", cycle or "нет")


def task2(forward=2, backward=-2):
    # На рисунке метки встречных дуг 2 и 4 наложены.
    # Рабочее прочтение: 4 -> 2 = -2, 2 -> 4 = 2.
    edges = [(1,2,5), (1,3,10), (2,3,3), (2,4,forward), (4,2,backward),
             (3,4,2), (3,5,7), (4,5,4), (5,1,12)]
    matrix = [[0 if i == j else inf for j in range(5)] for i in range(5)]
    for u, v, w in edges:
        matrix[u-1][v-1] = w
    print("Исходная матрица:")
    show_matrix(matrix)
    result = floyd(matrix)
    if any(result[i][i] < 0 for i in range(5)):
        _, _, cycle = bellman(range(1, 6), edges, 1)
        print("Отрицательный цикл:", cycle)
        print("Граф сильно связен: конечных минимумов нет ни для одной пары.")
        return
    print("Матрица расстояний:")
    show_matrix(result)
    print("Отрицательный цикл:", any(result[i][i] < 0 for i in range(5)))


def task3():
    rates = {('USD','EUR'):0.85, ('EUR','GBP'):1.15, ('GBP','USD'):1.05,
             ('USD','JPY'):145, ('JPY','GBP'):0.0075}
    weights = [(u, v, -log(rate)) for (u, v), rate in rates.items()]
    _, _, cycle = bellman(['USD','EUR','GBP','JPY'], weights, 'USD')
    if cycle:
        # Записываем найденный цикл начиная с доллара.
        body = cycle[:-1]
        k = body.index('USD')
        cycle = body[k:] + body[:k] + ['USD']
        factor = prod(rates[u, v] for u, v in zip(cycle, cycle[1:]))
        print("Цикл:", " -> ".join(cycle))
        print(f"Коэффициент: {factor:.6f}")
        print(f"Из 1000 USD получено {1000*factor:.4f} USD")
        print(f"Чистая прибыль: {1000*(factor-1):.4f} USD")
    else:
        print("Арбитраж отсутствует")


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--forward', type=int, default=2, help='вес 2 -> 4')
    parser.add_argument('--backward', type=int, default=-2, help='вес 4 -> 2')
    args = parser.parse_args()
    for number, task in enumerate([task1, task2, task3], 1):
        print(f"Задание {number}")
        if number == 2:
            task(args.forward, args.backward)
        else:
            task()
