import sys
from PyQt5 import QtWidgets
from GUI.GUI import Ui_MainWindow, Digits
from pyqt_sudoku_utils.game_results import GameResults
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
        self._history.reset(self._cells_value)
        self._timer.reset()
        self._timer.start()
        self._game_results = GameResults(self.cells, self._const_cells, self._cells_value, self._solve)
        self._records.update_connection()

    def _generate_sudoku_map(self):
        N = 3
        field = generate(N)
        self._is_fail = self._is_game_over = False
        self._cells_value = [cell for row in field for cell in row]
        self._solve = [cell for row in next(solve_sudoku((N, N), field)) for cell in row]
        self._const_cells = [bool(cell) for cell in self._cells_value]

    def _set_button_style_and_text(self):
        for i in range(len(self.cells)):
            button = self.cells[i]
            if self._const_cells[i]:
                style = """
                           QPushButton { background-color: yellow; }
                           QPushButton:pressed { background-color: red; }
                        """
                button.setText(str(self._cells_value[i]))
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

        if self._is_game_over or self._const_cells[index]:
            return

        digit = self._get_user_digit()
        if not digit:
            return

        button.setText(digit)

        self._history.update_moves_history(index, digit)
        self._cells_value[index] = int(digit)

        if self._is_fail and self._cells_value[index] == self._solve[index]:
            button.setStyleSheet("background-color: green")

        res = self._game_results.check_result()
        if res == "win":
            self._is_game_over = True
            self._history.end_game()
            self._game_results.win(self)
        elif res == "fail" and not self._game_results.is_fail:
            self._fail()

    def _fail(self):
        error_dialog = QtWidgets.QErrorMessage(self)
        error_dialog.showMessage("Судоку заполнено неверно")
        self._is_fail = True
        self._game_results.fail()

    @staticmethod
    def _get_user_digit():
        window = Digits()
        window.exec()
        return window.num

    def closeEvent(self, event):
        self._timer.cancel()
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Sudoku()
    ex.show()
    sys.exit(app.exec_())
