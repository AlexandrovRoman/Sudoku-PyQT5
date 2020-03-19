from utils.infinity_call import InfiniteTimer


class Timer:
    def __init__(self, time_label):
        self._time_label = time_label
        self._seconds = self._minutes = 0
        self._th_timer = InfiniteTimer(1, self.update_time)

    def reset(self):
        self._seconds = self._minutes = 0

    def start(self):
        self._th_timer.start()

    def cancel(self):
        try:
            self._th_timer.cancel()
        except AttributeError:
            pass

    @staticmethod
    def ftime(seconds, minutes=0):
        return "0" * (2 - len(str(minutes))) + str(minutes) + ":" + "0" * (
                    2 - len(str(seconds))) + str(seconds)

    def update_time(self):
        if self._minutes == self._seconds == 59:
            return
        self._seconds += 1
        if self._seconds == 60:
            self._minutes += 1
            self._seconds -= 60
        self._time_label.setText(self.ftime(self._seconds, self._minutes))

    @property
    def minutes(self):
        return self._minutes

    @property
    def seconds(self):
        return self._seconds
