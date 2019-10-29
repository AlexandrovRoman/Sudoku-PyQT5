import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from GUI.GUI import Ui_MainWindow, Digits
from utils.sudoku_generator import generate
from utils.solver import solve_sudoku
from CallFunc.Call import InfiniteTimer
from RecordsToPickle.pickle_record import save, get, sorted_records
from collections import deque


class Sudoku(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.new_game_button.clicked.connect(self.new_game)
        # self.next_button.clicked.connect(self.next)
        # self.back_button.clicked.connect(self.back)
        self.new_game()
        self.records()

    def new_game(self):
        N = 3
        field = generate(N)
        self.is_fail = False
        self.field_value = [cell for row in field for cell in row]
        self.solve = [cell for row in next(solve_sudoku((N, N), field)) for cell in row]
        self.cell_const = [bool(cell) for cell in self.field_value]
        for i in range(len(self.field)):
            button = self.field[i]
            if self.field_value[i]:
                style = """
                           QPushButton { background-color: yellow }
                           QPushButton:pressed { background-color: red; }
                        """
                button.setText(str(self.field_value[i]))
            else:
                style = """
                           QPushButton { background-color: white }
                           QPushButton:hover { background-color: silver; }
                        """
                button.setText("")
                button.clicked.connect(self.clicked)
            button.setStyleSheet(style)
        try:
            self.timer.cancel()
        except AttributeError:
            pass
        self.moves_history = deque(maxlen=3)
        self.cursor = self.seconds = self.minutes = 0
        self.timer = InfiniteTimer(1, self.set_time)
        self.timer.start()

    def records(self):
        for index, item in enumerate(sorted_records(get())):
            QtWidgets.QListWidgetItem(f"{index + 1}. {item}", self.listWidget)

    def set_time(self):
        self.seconds += 1
        if self.seconds == 60:
            self.minutes += 1
            self.seconds -= 60
        self.time_label.setText("0" * (2 - len(str(self.minutes))) + str(self.minutes) + ":" +
                                "0" * (2 - len(str(self.seconds))) + str(self.seconds))

    def clicked(self):
        button = self.sender()
        window = Digits()
        window.exec()
        digit = window.num
        if not digit: return
        button.setText(digit)
        index = self.field.index(button)
        # if self.cursor != len(self.moves_history):
        #     self.moves_history = self.moves_history[:self.cursor + 1]
        # self.moves_history.append((index, digit))
        # self.cursor = len(self.moves_history) - 1
        self.field_value[index] = int(digit)
        if self.field_value[index] == self.solve[index] and self.is_fail:
            button.setStyleSheet("background-color: green")
        self.result()

    # def next(self):
    #     if self.cursor < 3:
    #         self.cursor += 1
    #         self.set_field()
    #
    # def back(self):
    #     if self.cursor > 0:
    #         self.cursor -= 1
    #         self.set_field()
    #
    # def set_field(self):
    #     index, value = self.moves_history[self.cursor]
    #     self.field_value[index] = value
    #     if value != 0: self.field[index].setText(str(value))

    def result(self):
        if not all(self.field_value): return
        if self.field_value != self.solve:
            if not self.is_fail:
                return self.fail()
        else:
            return self.win()

    def win(self):
        self.time.cancel()
        win_dialog = QtWidgets.QErrorMessage(self)
        win_dialog.showMessage(f"Победа! Ваше время {self.time_label.text()}")
        if not self.is_fail:
            save(self.time_label.text())
            self.records()

    def fail(self):
        self.is_fail = True
        error_dialog = QtWidgets.QErrorMessage(self)
        error_dialog.showMessage("Судоку заполнено неверно")
        for i in range(len(self.field_value)):
            if self.field_value[i] != self.solve[i]:
                self.field[i].setStyleSheet("background-color: red")
            else:
                if not self.cell_const[i]: self.field[i].setStyleSheet("background-color: green")

    def closeEvent(self, event):
        self.timer.cancel()
        event.accept()


app = QtWidgets.QApplication(sys.argv)
ex = Sudoku()
ex.show()
sys.exit(app.exec_())

