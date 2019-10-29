from pickle import dump, load


def sorted_records(data):
    return sorted(data, key=lambda time: int(time.split(":")[0]) * 60 + int(time.split(":")[1]))[:10]


def save(data):
    from os import mkdir
    data_deq = get()
    data_deq.append(data)
    data_deq = sorted_records(data_deq)
    try:
        with open("records/records.pickle", "wb") as f:
            dump(data_deq, f)
    except FileNotFoundError:
        mkdir("./records")
        save(data)


def get():
    from collections import deque
    try:
        with open('records/records.pickle', 'rb') as f:
            return deque(set(load(f)), maxlen=10)
    except FileNotFoundError:
        return deque(maxlen=10)
