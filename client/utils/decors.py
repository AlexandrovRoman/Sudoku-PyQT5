from threading import Thread


def to_async(func):
    def wrapper(*args, **kwargs):
        if args and kwargs:
            th = Thread(target=func, args=args, kwargs=kwargs, daemon=True)
        elif args:
            th = Thread(target=func, args=args, daemon=True)
        elif kwargs:
            th = Thread(target=func, kwargs=kwargs, daemon=True)
        else:
            th = Thread(target=func, daemon=True)
        th.start()
    return wrapper
