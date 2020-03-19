from flask import render_template, request
from sudoku.utils import get_records, valid_record, add_record


def index():
    return "Hello, this sudoku project"


def top(n):
    try:
        n = min((200, int(n)))
    except ValueError:
        n = 200
    return render_template("sudoku_records.html", records=get_records(n))


def new_record():
    name = request.json["nick"]
    time = int(request.json["time"])
    if not valid_record(name, time):
        return "Not add"
    add_record(name, time)
    return "Add"
