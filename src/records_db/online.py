import requests

URL = "http://alexandrovroman.pythonanywhere.com/"
SUDOKU_URL = "sudoku/"


def has_connect() -> bool:
    try:
        return requests.get(URL).status_code == 200
    except requests.exceptions.ConnectionError:
        return False


def top(n: int) -> list:
    json = {"n": n}
    response = requests.post(URL + SUDOKU_URL + "top", json=json)
    rows = response.text.split("\n")[:-1]  # Сервер возвращает в конце пустую строку, поэтому ее не берем

    matrix = []
    for row in rows:
        nick, ftime = row.split(": ")  # ftime - format_time
        matrix.append(tuple([nick, ftime]))
    return matrix


def add_record(nick: str, time: int) -> None:
    """ Добавляет ваш рекорд """
    json = {"nick": nick, "time": time}
    requests.post(URL + SUDOKU_URL + "add", json=json)
