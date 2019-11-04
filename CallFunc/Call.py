from threading import Timer


class InfiniteTimer:
    """ Класс таймера который не останавливается, пока вы этоо не захотите """

    def __init__(self, seconds, target):
        self._should_continue = False
        self.is_running = False
        self.seconds = seconds
        self.target = target
        self.thread = None

    def _handle_target(self):
        """ Запуск переданной функции """
        self.is_running = True
        self.target()
        self.is_running = False
        self._start_timer()

    def _start_timer(self):
        """ Запуск таймера (вспомогательная функция) """
        if self._should_continue:  # Если таймер работает
            self.thread = Timer(self.seconds, self._handle_target)
            self.thread.start()

    def start(self):
        """ Запуск таймера """
        if not self._should_continue and not self.is_running:
            self._should_continue = True
            self._start_timer()

    def cancel(self):
        """ Остановка таймера """
        if self.thread is not None:
            self._should_continue = False  # Отменить выполнение работы в любом случаее
            self.thread.cancel()


if __name__ == '__main__':
    def hello():
        print("Hello world!")


    t = InfiniteTimer(0.5, hello)
    t.start()
