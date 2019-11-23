def connect_db():
    """ Импортируем функции из нужных файлов в зависимости от того, есть ли подключение """
    from records_db.online import has_connect
    if has_connect():
        import records_db.online as func
        CONNECT = True
    else:
        import records_db.offline as func
        CONNECT = False
    return func.top, func.add_record, CONNECT
