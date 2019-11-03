import sqlite3


def top_15():
    data = sorted(get_records(), key=lambda record: record[1])
    return [
        (nick,
         "0" * (2 - len(str(time // 60))) + str(time // 60) + ":" +
         "0" * (2 - len(str(time % 60))) + str(time % 60))
        for nick, time in data[:15]]


def get_records():
    with sqlite3.connect("records_db/records.db") as con:
        cur = con.cursor()
        result = cur.execute("""
            SELECT NickName, Time FROM Records
            """).fetchall()
    return result


def add_record(nick, time):
    if not validation(nick, time) or not not_repeat(nick, time): return
    with sqlite3.connect("records_db/records.db") as con:
        con.execute(f"""
            INSERT INTO Records(NickName, Time) VALUES(?, ?)
            """, (nick, time))


def validation(nick, time):
    return isinstance(nick, str) and isinstance(time, int)


def not_repeat(nick, time):
    return (nick, time) not in get_records()


if __name__ == '__main__':
    add_record("Nikita", 1234)
    print(top_15())
