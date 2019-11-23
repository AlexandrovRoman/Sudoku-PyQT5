from random import randrange, choice
from utils.solver import solve_sudoku
from copy import deepcopy


class Grid:
    def __init__(self, n=3):
        """ Генерирование базовой таблицы """
        self.n = n
        self.table = [
            [
                ((i * n + i // n + j) % (n * n) + 1)
                for j in range(n * n)
            ]
            for i in range(n * n)
        ]

    def transposing(self):
        """ Транспонирование таблицы """

        self.table = map(list, zip(*self.table))
        self.table = list(self.table)

    def swap_rows_small(self):
        """ Меняет два ряда в пределах одного района местами """
        area = randrange(0, self.n, 1)
        line1 = randrange(0, self.n, 1)
        # получение случайного района и случайной строки
        N1 = area * self.n + line1
        # номер 1 строки для обмена

        line2 = randrange(0, self.n, 1)
        # случайная строка, но не та же самая
        while line1 == line2:
            line2 = randrange(0, self.n, 1)

        N2 = area * self.n + line2

        # номер 2 строки для обмена
        self.table[N1], self.table[N2] = self.table[N2], self.table[N1]

    def swap_colums_small(self):
        """  Меняет две колонки в пределах одного района местами """
        self.transposing()
        self.swap_rows_small()
        self.transposing()

    def swap_rows_area(self):
        """ Меняет два района по горизонтали местами """
        area1 = randrange(0, self.n, 1)
        # получение случайного района

        area2 = randrange(0, self.n, 1)
        # ещё район, но не тот же самый
        while area1 == area2:
            area2 = randrange(0, self.n, 1)

        for i in range(0, self.n):
            N1, N2 = area1 * self.n + i, area2 * self.n + i
            self.table[N1], self.table[N2] = self.table[N2], self.table[N1]

    def swap_colums_area(self):
        """ Меняет два района по вертикали местами """
        self.transposing()
        self.swap_rows_area()
        self.transposing()

    def mix(self, amt=10) -> None:
        """
        Функция генерации путем вызова различных методо перемешивания
        :param amt: int - количество перемешиваний
        :return: None
        """
        mix_func = [self.transposing,
                    self.swap_rows_small,
                    self.swap_colums_small,
                    self.swap_rows_area,
                    self.swap_colums_area]
        for i in range(1, amt):
            # Вызываем случайную функцию
            choice(mix_func)()


def generate(n=3) -> list:
    """
    Функция генерации таблицы судоку.
    :param n: int - размер базового поля
    :return: list - готовая таблица
    """

    grid = Grid(n)
    grid.mix()

    field_is_look = [
        [0 for _ in range(grid.n * grid.n)]
        for _ in range(grid.n * grid.n)
    ]
    difficult = grid.n ** 4  # Первоначально все элементы на месте

    iterator = grid.n ** 4 - 30

    while iterator < grid.n ** 4:
        # Выбираем случайную ячейку
        i, j = randrange(0, grid.n * grid.n, 1), randrange(0, grid.n * grid.n, 1)
        if field_is_look[i][j] == 0:  # Если её не смотрели
            iterator += 1
            field_is_look[i][j] = 1  # Посмотрим

            temp = grid.table[i][j]  # Сохраним элемент на случай если без него нет решения или их слишком много
            grid.table[i][j] = 0  # Удаляем элемент
            difficult -= 1  # Усложняем если убрали элемент

            table_solution = deepcopy(grid.table)  # Скопируем в отдельный список

            number_of_solution = len(list(solve_sudoku((grid.n, grid.n), table_solution)))  # Считаем количество решений

            if number_of_solution != 1:  # Если решение не одинственное вернуть всё обратно
                grid.table[i][j] = temp
                difficult += 1  # Облегчаем

    return grid.table

