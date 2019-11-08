import sys
from PyQt5 import QtWidgets
from GUI.GUI import Ui_MainWindow, Digits
from GUI.win_true import WinDialog
from utils.sudoku_generator import generate
from utils.solver import solve_sudoku
from CallFunc.Call import InfiniteTimer
from records_db.database import connect_db


# Заглушки для бд, чтобы реализовать кнопку реконнекта
top = lambda n: []
add_record = lambda nick, time: None
CONNECT = None


class Sudoku(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.new_game_button.clicked.connect(self.new_game)
        self.next_button.clicked.connect(self.next)
        self.back_button.clicked.connect(self.back)
        self.connect.clicked.connect(self.connect_)
        self.button_connect()
        self.connect_()
        self.records()
        self.new_game()

    def button_connect(self):
        """ Привязка всех кнопок """
        for button in self.field:
            button.clicked.connect(self.clicked)

    def new_game(self):
        """ Запуск новой игры """
        # количество клеток в мини поле
        N = 3
        field = generate(N)
        self.is_fail = self.is_game_over = False
        self.field_value = [cell for row in field for cell in row]
        self.solve = [cell for row in next(solve_sudoku((N, N), field)) for cell in row]
        self.cell_const = [bool(cell) for cell in self.field_value]

        # Изменение стиля и текста кнопок в зависимости от того, является ли ячейка изначально сгенерированной
        for i in range(len(self.field)):
            button = self.field[i]
            if self.cell_const[i]:
                style = """
                           QPushButton { background-color: yellow; }
                           QPushButton:pressed { background-color: red; }
                        """
                button.setText(str(self.field_value[i]))
            else:
                style = """
                           QPushButton { background-color: white; }
                           QPushButton:hover { background-color: silver; }
                        """
                button.setText("")
            button.setStyleSheet(style)

        self.moves_history = []
        self.deep_immersion = -1

        # Отключение таймера, если он был включен ранее
        try:
            self.timer.cancel()
        except AttributeError:
            pass
        # Обнуление количества минут и секунд, запуск таймера
        self.seconds = self.minutes = 0
        self.timer = InfiniteTimer(1, self._set_time)
        self.timer.start()

    def records(self):
        """ Вывод списка лучших игр (топ 15) """
        self.listWidget.clear()  # Отчистка на случай обновления
        for index, item in enumerate(top(15)):
            QtWidgets.QListWidgetItem(f"{index + 1}. {' - '.join(item)}", self.listWidget)

    def connect_(self):
        global top, add_record, CONNECT
        if CONNECT:  # Если есть соединение, зачем что-то менять
            return
        top, add_record, CONNECT = connect_db()
        self._set_db_button()
        self.records()

    def _set_db_button(self):
        if CONNECT:
            color = "#00e600"
            text = "Есть контакт)))"
        else:
            color = "#ff2400"
            text = "Соединение\nотсутствует((("
        self.connect.setStyleSheet(" QPushButton { background-color: " + color + "; } ")
        self.connect.setText(text)

    def _set_time(self):
        """ Прибавить секунду ко времени """
        # Время всегда будет меньше часа, т.к. час на судоку... Очень много
        if self.minutes == self.seconds == 59:
            return
        self.seconds += 1
        if self.seconds == 60:
            self.minutes += 1
            self.seconds -= 60
        self.time_label.setText("0" * (2 - len(str(self.minutes))) + str(self.minutes) + ":" +
                                "0" * (2 - len(str(self.seconds))) + str(self.seconds))

    def clicked(self):
        """ Изменение значения ячейки на которую нажал пользователь """
        button = self.sender()
        index = self.field.index(button)
        # Если пользователь окончил игру или ячейка не подлежит изменению
        if self.is_game_over or self.cell_const[index]:
            return

        # Создание диалогового окна и получение цифры
        window = Digits()
        window.exec()
        digit = window.num
        if not digit:
            return
        button.setText(digit)

        # если глубина погружения отличается от стандартной
        if self.deep_immersion != -1:

            # Оставляем от массива только часть после глубины погружения
            self.moves_history = self.moves_history[self.deep_immersion + 1:]

            # Возвращаем глубину к стандартному значению
            self.deep_immersion = -1

        # Вставляем в начало массива текущий ход в формате (index, last_value, current_value)
        self.moves_history.insert(0, (index, self.field_value[index], int(digit)))

        self.field_value[index] = int(digit)
        if self.is_fail and self.field_value[index] == self.solve[index]:
            button.setStyleSheet("background-color: green")

        # Проверяем окончена ли игра
        self.result()

    def next(self):
        """ Следующий ход (кнопка вперед) """
        if self.is_game_over:
            return
        # Если есть значения дальше
        if self.deep_immersion >= 0:
            self._set_field(True)
            self.deep_immersion -= 1

    def back(self):
        """ Предыдуший ход (кнопка назад) """
        if self.is_game_over:
            return
        # Если есть значения до
        if self.deep_immersion < len(self.moves_history) - 1:
            self.deep_immersion += 1
            self._set_field(False)

    def _set_field(self, is_next):
        """ Изменяет значение на прошлое лил следующее (is_next) """
        index, *values = self.moves_history[self.deep_immersion]
        # Если следующее - берем current_value (стр. 107) иначе прошлое
        value = values[1] if is_next else values[0]
        self.field_value[index] = value
        if value != 0:
            self.field[index].setText(str(value))
        else:
            self.field[index].setText("")

    def result(self):
        """ Проверка резултата """
        # Если не все клетки запонены - выходим
        if not all(self.field_value):
            return
        if self.field_value != self.solve:
            # Если окно поражения не вызывалось
            if not self.is_fail:
                return self.fail()
        else:
            return self.win()

    def win(self):
        """ Функция успешного завершения игры """
        # Останавливаем таймер и сообщаем о завершении игры
        self.timer.cancel()
        self.is_game_over = True

        # Если игра не была до этого проиграна
        if not self.is_fail:
            # Поздравление и запись рекорда в бд
            win_dialog = WinDialog()
            if win_dialog.exec_():
                add_record(win_dialog.nick, self.minutes * 60 + self.seconds)
                self.records()
        else:
            # Иначе сообщение о победе без записи в таблицу рекордов
            win_dialog = QtWidgets.QErrorMessage(self)
            win_dialog.showMessage(f"Победа! Ваше время {self.time_label.text()}")

    def fail(self):
        """ Поражение """
        self.is_fail = True  # Игра проиграна

        # Сообщение о поражении
        error_dialog = QtWidgets.QErrorMessage(self)
        error_dialog.showMessage("Судоку заполнено неверно")
        # Смена цвета ячеек в зависимости от правильности заполнения
        for i in range(len(self.field_value)):
            if self.field_value[i] != self.solve[i]:
                self.field[i].setStyleSheet("background-color: red")
            else:
                if not self.cell_const[i]:
                    self.field[i].setStyleSheet("background-color: green")

    def closeEvent(self, event):
        """ Закрытие игры (изменено для остановки таймера) """
        self.timer.cancel()
        event.accept()


# Т.к. это скрипт - if __name__ == '__main__' не используется
app = QtWidgets.QApplication(sys.argv)
ex = Sudoku()
ex.show()
sys.exit(app.exec_())
