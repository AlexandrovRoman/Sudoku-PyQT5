import sqlite3


def get_records(n):
    with sqlite3.connect("records.db") as con:
        cur = con.cursor()
        result = cur.execute("""
                                SELECT NickName, Time FROM Records
                                ORDER BY Time
                                """).fetchall()
    records = []
    for nick, time in result:
        minutes = time // 60
        seconds = time % 60
        str_time = "0" * (2 - len(str(minutes))) + str(minutes) + ":" + "0" * (2 - len(str(seconds))) + str(seconds)
        records.append({"nick": nick, "time": str_time})
    return records[:n]


def valid_record(name, time):
    return isinstance(name, str) and isinstance(time, int) and valid_name(name)


def valid_name(name):
    return " " not in name and no_sql_commands(name)


def no_sql_commands(string):
    commands = ["CREATE", "ALTER", "DROP", "INSERT", "UPDATE", "DELETE", "SELECT", "FROM", "WHERE", "OR", "ORDER", "BY",
                "AND"]
    return not any([command in string for command in commands])


def add_record(nick, time):
    with sqlite3.connect("records.db") as con:
        con.execute(f"INSERT INTO Records(NickName, Time) VALUES(?, ?)", (nick, time))
