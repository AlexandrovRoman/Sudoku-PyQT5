from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QGridLayout, QPushButton, QLabel
from PyQt5 import QtCore, QtWidgets


class Ui_MainWindow(object):
    """ В данном классе я не менял почти ничего,
    за исключением преобразования кнопок из отдельных переменных в массив """
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Sudoku")
        MainWindow.resize(339, 418)


        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 341, 371))
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")

        gridLayoutWidget = QtWidgets.QWidget(self.tab)
        gridLayoutWidget.setGeometry(QtCore.QRect(0, 60, 331, 286))
        gridLayoutWidget.setObjectName("gridLayoutWidget")

        main_layout = QGridLayout(gridLayoutWidget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        positions = [(i, j) for i in range(9) for j in range(9)]

        font = QFont('Arial', 14)
        self.field = []
        for position in positions:
            btn = QPushButton()
            btn.setMaximumSize(QtCore.QSize(30, 30))
            btn.setFont(font)
            main_layout.addWidget(btn, *position)
            self.field.append(btn)

        self.time_label = QLabel(self.tab)
        self.time_label.setGeometry(QtCore.QRect(90, 0, 61, 51))

        self.back_button = QPushButton(self.tab)
        self.back_button.setGeometry(QtCore.QRect(170, 0, 61, 51))
        self.back_button.setObjectName("back_button")

        self.next_button = QtWidgets.QPushButton(self.tab)
        self.next_button.setGeometry(QtCore.QRect(250, 0, 61, 51))
        self.next_button.setObjectName("next_button")

        self.new_game_button = QtWidgets.QPushButton(self.tab)
        self.new_game_button.setGeometry(QtCore.QRect(10, 0, 71, 51))
        self.new_game_button.setObjectName("new_game_button")

        self.tabWidget.addTab(self.tab, "")

        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.listWidget = QtWidgets.QListWidget(self.tab_2)
        self.listWidget.setGeometry(QtCore.QRect(0, 30, 341, 321))
        self.listWidget.setObjectName("listView")

        self.best_rounds = QLabel(self.tab_2)
        self.best_rounds.setGeometry(QtCore.QRect(0, 0, 81, 31))
        self.best_rounds.setObjectName("label")

        self.tabWidget.addTab(self.tab_2, "")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 339, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Судоку"))
        self.time_label.setText('Time\nTo\nWin')
        self.back_button.setText(_translate("MainWindow", "↶"))
        self.next_button.setText(_translate("MainWindow", "↷"))
        self.new_game_button.setText(_translate("MainWindow", "Новая игра"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Игра"))
        self.best_rounds.setText(_translate("MainWindow", "Лучшие раунды"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2),
                                  _translate("MainWindow", "Турнирная таблица"))


class Digits(QDialog):
    """ Класс Digit - диалоговое окно получающее от пользователя цифру. Сделан по макету Alphabet """
    def __init__(self, *args):
        super().__init__(*args)

        self.num = None
        self.setWindowTitle('Выберите цифру')
        self.__digits = "123456789"
        self.init_ui()

    def init_ui(self):
        main_layout = QGridLayout()
        font = QFont('Arial', 14)

        positions = [(i, j) for i in range(3) for j in range(3)]

        for position, letter in zip(positions, self.__digits):
            btn = QPushButton(letter)
            btn.setFont(font)
            btn.clicked.connect(self.on_click)
            btn.setMaximumSize(QtCore.QSize(40, 40))
            main_layout.addWidget(btn, *position)

        self.setLayout(main_layout)

    def on_click(self):
        btn = self.sender()
        self.num = btn.text()
        self.close()
