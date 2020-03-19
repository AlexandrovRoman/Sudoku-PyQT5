from records_db.database import connect_db
from PyQt5 import QtWidgets
from utils.decors import to_async


class Records:
    def __init__(self, record_widget, update_connect_button):
        self._connect = False
        self._record_widget = record_widget
        self._update_connect_button = update_connect_button
        self.update_connection()

    @to_async
    def update_connection(self, _=False):
        self._top, self.add_record, cur_connect = connect_db()
        # Если ничего не изменилось выходим из функции
        if cur_connect == self._connect:
            return
        self._connect = cur_connect
        self._set_db_button()
        self.update_records_widget()

    def _set_db_button(self):
        if self._connect:
            color = "#00e600"
            text = "Есть контакт)))"
        else:
            color = "#ff2400"
            text = "Соединение\nотсутствует((("
        self._update_connect_button.setStyleSheet(" QPushButton { background-color: " + color + "; } ")
        self._update_connect_button.setText(text)

    def update_records_widget(self):
        self._record_widget.clear()
        self.update_connection()
        for index, item in enumerate(self._top(100)):
            QtWidgets.QListWidgetItem(f"{index + 1}. {' - '.join(item)}", self._record_widget)
