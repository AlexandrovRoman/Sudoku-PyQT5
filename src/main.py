import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from GUI.GUI import Ui_MainWindow, Digits
from GUI.win_true import WinDialog
from pyqt_sudoku_utils.history import History
from pyqt_sudoku_utils.records import Records
from pyqt_sudoku_utils.timer import Timer
from utils.sudoku_generator import generate
from utils.solver import solve_sudoku


class Sudoku(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.new_game_button.clicked.connect(self.new_game)

        self._button_bind()

        self._records = Records(self.listWidget, self.connect_button)
        self.connect_button.clicked.connect(self._records.update_connection)

        self._timer = Timer(self.time_label)

        self._history = History(self.cells)
        self.next_button.clicked.connect(self._history.next_move)
        self.back_button.clicked.connect(self._history.back_move)

        self.new_game()

    def _button_bind(self):
        for button in self.cells:
            button.clicked.connect(self._clicked)

    def new_game(self):
        self._generate_sudoku_map()

        self._set_button_style_and_text()

        self._history.reset(self.cells_value)

        self._timer.reset()

    def _generate_sudoku_map(self):
        N = 3
        field = generate(N)
        self.is_fail = self.is_game_over = False
        self.cells_value = [cell for row in field for cell in row]
        self.solve = [cell for row in next(solve_sudoku((N, N), field)) for cell in row]
        self.const_cells = [bool(cell) for cell in self.cells_value]

    def _set_button_style_and_text(self):
        for i in range(len(self.cells)):
            button = self.cells[i]
            if self.const_cells[i]:
                style = """
                           QPushButton { background-color: yellow; }
                           QPushButton:pressed { background-color: red; }
                        """
                button.setText(str(self.cells_value[i]))
            else:
                style = """
                           QPushButton { background-color: white; }
                           QPushButton:hover { background-color: silver; }
                        """
                button.setText("")
            button.setStyleSheet(style)

    def _clicked(self):
        button = self.sender()
        index = self.cells.index(button)
        # Если пользователь окончил игру или ячейка не подлежит изменению
        if self.is_game_over or self.const_cells[index]:
            return

        digit = self._get_user_digit()
        if not digit:
            return
        button.setText(digit)

        self._history.update_moves_history(index, digit)

        if self.is_fail and self.cells_value[index] == self.solve[index]:
            button.setStyleSheet("background-color: green")

        self._check_result()

    @staticmethod
    def _get_user_digit():
        window = Digits()
        window.exec()
        return window.num

    def _check_result(self):
        """ Проверка резултата """
        # Если не все клетки запонены - выходим
        if not all(self.cells_value):
            return

        if self.cells_value != self.solve:
            if not self.is_fail:
                return self._fail()
        else:
            return self._win()

    def _win(self):
        """ Функция успешного завершения игры """
        # Останавливаем таймер и сообщаем о завершении игры
        self.is_game_over = True
        self._history.end_game()

        # Если игра не была до этого проиграна
        if not self.is_fail:
            # Поздравление и запись рекорда в бд
            win_dialog = WinDialog()
            if win_dialog.exec_() and win_dialog.nick:
                self._records.update_connection()
                self._records.add_record(win_dialog.nick, self._timer.minutes * 60 + self._timer.seconds)
                self._records._update_records_widget()
        else:
            # Иначе сообщение о победе без записи в таблицу рекордов
            win_dialog = QtWidgets.QErrorMessage(self)
            win_dialog.showMessage(f"Победа! Ваше время {self.time_label.text()}")

    def _fail(self):
        """ Поражение """
        self.is_fail = True  # Игра проиграна

        # Сообщение о поражении
        error_dialog = QtWidgets.QErrorMessage(self)
        error_dialog.showMessage("Судоку заполнено неверно")
        # Смена цвета ячеек в зависимости от правильности заполнения
        for i in range(len(self.cells_value)):
            if self.cells_value[i] != self.solve[i]:
                self.cells[i].setStyleSheet("background-color: red")
            else:
                if not self.const_cells[i]:
                    self.cells[i].setStyleSheet("background-color: green")

    def closeEvent(self, event):
        """ Закрытие игры (изменено для остановки таймера) """
        self.timer.cancel()
        event.accept()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Sudoku()
    timer = QTimer()
    timer.timeout.connect(ex._timer.update_time)
    ex.show()
    timer.start(1000)
    sys.exit(app.exec_())
