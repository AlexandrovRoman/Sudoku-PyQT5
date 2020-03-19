def connect_db():
    """ Импортируем функции из нужных файлов в зависимости от того, есть ли подключение """
    from records_db.online import has_connect
    if has_connect():
        import records_db.online as db_module
        CONNECT = True
    else:
        import records_db.offline as db_module
        CONNECT = False
    return db_module.top, db_module.add_record, CONNECT
