class Timer:
    def __init__(self, time_label):
        self._time_label = time_label
        self._seconds = self._minutes = 0

    def reset(self):
        self._seconds = self._minutes = 0

    def update_time(self):
        if self._minutes == self._seconds == 59:
            return
        self._seconds += 1
        if self._seconds == 60:
            self._minutes += 1
            self._seconds -= 60
        self._time_label.setText("0" * (2 - len(str(self._minutes))) + str(self._minutes) + ":" +
                                 "0" * (2 - len(str(self._seconds))) + str(self._seconds))

    @property
    def minutes(self):
        return self._minutes

    @property
    def seconds(self):
        return self._seconds
