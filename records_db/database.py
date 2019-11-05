import sqlite3


def top(n):
    """ Возвращает n лучших игр """
    # Берем первые n из всех и возвращаем в красивом формате
    return [
        (nick,
         "0" * (2 - len(str(time // 60))) + str(time // 60) + ":" +
         "0" * (2 - len(str(time % 60))) + str(time % 60))
        for nick, time in get_records()[:n]]


def get_records():
    """ Получаем отсортированные рекорды """
    with sqlite3.connect("records_db/records.db") as con:
        cur = con.cursor()
        result = cur.execute("""
            SELECT NickName, Time FROM Records
            ORDER BY Time
            """).fetchall()
    return result


def add_record(nick, time):
    """ Добавляем рекорд в базу """
    # Проверка на корректность
    if not validation(nick, time) or not not_repeat(nick, time):
        return
    with sqlite3.connect("records_db/records.db") as con:
        con.execute(f"""
            INSERT INTO Records(NickName, Time) VALUES(?, ?)
            """, (nick, time))


def validation(nick, time):
    return isinstance(nick, str) and isinstance(time, int)


def not_repeat(nick, time):
    return (nick, time) not in get_records()
