from itertools import product


def solve_sudoku(size, grid):
    """ Решатель судоку с помощью алгоритма X """
    R, C = size
    N = R * C
    # заполняем строки
    X = ([("rc", rc) for rc in product(range(N), range(N))] +
         [("rn", rn) for rn in product(range(N), range(1, N + 1))] +
         [("cn", cn) for cn in product(range(N), range(1, N + 1))] +
         [("bn", bn) for bn in product(range(N), range(1, N + 1))])
    # заполняем столбцы
    Y = dict()
    for r, c, n in product(range(N), range(N), range(1, N + 1)):
        b = (r // R) * R + (c // C)  # Box number
        Y[(r, c, n)] = [
            ("rc", (r, c)),
            ("rn", (r, n)),
            ("cn", (c, n)),
            ("bn", (b, n))]
    X, Y = exact_cover(X, Y)
    for i, row in enumerate(grid):
        for j, n in enumerate(row):
            if n:
                select(X, Y, (i, j, n))
    # Идем по всевсевозможным решениям
    for solution in solve(X, Y, []):
        for (r, c, n) in solution:
            grid[r][c] = n
        yield grid


def exact_cover(X, Y):
    """ Форматирование данных строк """
    X = {j: set() for j in X}
    for i, row in Y.items():
        for j in row:
            X[j].add(i)
    return X, Y


def solve(X, Y, solution):
    """ Сам алгоритм """
    if not X:
        yield list(solution)
    else:
        # ищем столбец с минимальным числом элементов
        c = min(X, key=lambda x: len(X[x]))
        for r in list(X[c]):
            solution.append(r)
            cols = select(X, Y, r)
            for s in solve(X, Y, solution):
                yield s
            deselect(X, Y, r, cols)
            solution.pop()


def select(X, Y, r):
    bufer = []
    for j in Y[r]:
        # удаляем все пересекающиеся строки из всех оставшихся столбцов
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].remove(i)
        # вынимаем текущий столбец из таблицы в буфер
        bufer.append(X.pop(j))
    return bufer


def deselect(X, Y, r, cols):
    """ Удаляли столбцы от первого пересечения с r к последнему, восстанавливать надо в обратном порядке """
    for j in reversed(Y[r]):
        X[j] = cols.pop()
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].add(i)

