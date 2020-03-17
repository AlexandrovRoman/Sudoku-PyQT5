class History:
    def __init__(self, cells):
        self._cells = cells

    def reset(self, cells_value):
        self._cells_value = cells_value
        self._deep_immersion = -1
        self._moves_history = []
        self._is_game_over = False

    def end_game(self):
        self._is_game_over = True

    def update_moves_history(self, index, digit):
        if self._deep_immersion != -1:
            # Оставляем от массива только часть после глубины погружения
            self._moves_history = self._moves_history[self._deep_immersion + 1:]

            # Возвращаем глубину к стандартному значению
            self._deep_immersion = -1

        # Вставляем в начало массива текущий ход в формате (index, last_value, current_value)
        self._moves_history.insert(0, (index, self._cells_value[index], int(digit)))

    def next_move(self):
        """ Следующий ход (кнопка вперед) """
        if self._is_game_over or self._deep_immersion < 0:
            return
        self._set_move(True)
        self._deep_immersion -= 1

    def back_move(self):
        """ Предыдуший ход (кнопка назад) """
        if self._is_game_over or self._deep_immersion >= len(self._moves_history) - 1:
            return
        self._deep_immersion += 1
        self._set_move(False)

    def _set_move(self, is_next):
        """ Изменяет значение на прошлое или следующее (is_next) """
        index, *values = self._moves_history[self._deep_immersion]
        value = values[1] if is_next else values[0]
        self._cells_value[index] = value
        self._cells[index].setText(str(value) if value != 0 else "")
