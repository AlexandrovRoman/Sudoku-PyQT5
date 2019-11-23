# Судоку на PyQt5.
Дополнения к самому судоку:
+ Кнопки вперед/назад
+ Таблица рекордов (онлайн/офлайн)
+ Кнопка начала новой игры

## Скриншоты отражающие основные состояния программы:<br>
![Image alt](https://github.com/AlexandrovRoman/Sudoku-PyQT5/raw/master/Screenshots/game_field.jpg)*ᅠᅠ*
![Image alt](https://github.com/AlexandrovRoman/Sudoku-PyQT5/raw/master/Screenshots/win_dialog__not_fail.jpg)<br><br>
![Image alt](https://github.com/AlexandrovRoman/Sudoku-PyQT5/raw/master/Screenshots/fail_dialog.jpg)*ᅠᅠ*
![Image alt](https://github.com/AlexandrovRoman/Sudoku-PyQT5/raw/master/Screenshots/win_dialog__is_fail.jpg)<br><br>
![Image alt](https://github.com/AlexandrovRoman/Sudoku-PyQT5/raw/master/Screenshots/records__has_connect.jpg)*ᅠᅠ*
![Image alt](https://github.com/AlexandrovRoman/Sudoku-PyQT5/raw/master/Screenshots/records__has_not_connect.jpg)<br>

## Инструкция по установке:
1. Установка Python (https://www.python.org/downloads/) 
с добавлением в глобальную среду (при установке ставим галочку напротив Add Python to PATH)
2. Пишем в консоли команды: <br>
pip install pyqt5 <br>
pip install requests
3. Запускаем main.py

## Этапы разработки:
+ Создание интерфейса
+ Добавление кнопки новая игра
+ Создание таймера (thread)
+ Первая реализация рекордов (С помощью модуля pickle)
+ Вторая версия таблицы рекордов (sqlite, работает только локально)
+ Добавление кнопок вперед/назад (Наиболее сложный этап т.к. пришлось придумывать свой алгоритм)
+ Третья версия таблицы рекордов (Создание глобального сервера на Flask. Второй по сложности этап)

## Возможные доработки:
+ Добавить в алгоритм генерации возможность указывать сложность
+ Повысить безопасность сервера
+ Сделать отзывчивый дизайн
+ Собрать exe файл
