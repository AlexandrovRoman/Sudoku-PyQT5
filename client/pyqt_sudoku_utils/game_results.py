from typing import Tuple
from PyQt5 import QtWidgets
from GUI.win_true import WinDialog
from pyqt_sudoku_utils.records import Records


class GameResults:
    def __init__(self, cells, const_cells, cells_values, solve):
        self._cells = cells
        self._const_cells = const_cells
        self._cells_values = cells_values
        self._solve = solve
        self._is_fail = False

    def check_result(self):
        """ Проверка резултата """
        # Если не все клетки запонены - выходим
        if not all(self._cells_values):
            return "no result"

        if self._cells_values != self._solve:
            return "fail"
        else:
            return "win"

    def update_cell_value(self, cell_value, index):
        self._cells_values[index] = cell_value

    def win(self, sudoku):
        sudoku._timer.cancel()
        if not self._is_fail:
            # Поздравление и запись рекорда в бд
            win_dialog = WinDialog(sudoku._timer.ftime(sudoku._timer.seconds, sudoku._timer.minutes))
            if win_dialog.exec_() and win_dialog.nick:
                self._add_record(sudoku._records, (win_dialog.nick, sudoku._timer.minutes * 60 + sudoku._timer.seconds))
        else:
            # Иначе сообщение о победе без записи в таблицу рекордов
            win_dialog = QtWidgets.QErrorMessage(sudoku)
            win_dialog.showMessage(
                f"Победа! Ваше время: {sudoku._timer.ftime(sudoku._timer.seconds, sudoku._timer.minutes)}")

    @staticmethod
    def _add_record(records: Records, record: Tuple[str, int]):
        records.update_connection()
        records.add_record(*record)
        records.update_records_widget()

    def fail(self):
        self._is_fail = True

        for i in range(len(self._cells_values)):
            if self._cells_values[i] != self._solve[i]:
                self._cells[i].setStyleSheet("background-color: red")
            else:
                if not self._const_cells[i]:
                    self._cells[i].setStyleSheet("background-color: green")

    @property
    def is_fail(self):
        return self._is_fail
