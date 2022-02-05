from threading import Timer
import time


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self.__timer = None
        self.__interval = interval
        self.__function = function
        self.__args = args
        self.__kwargs = kwargs
        self.__is_running = False
        self.__next_call = time.time()
        self.start()

    def _run(self):
        self.__is_running = False
        self.start()
        self.__function(*self.__args, **self.__kwargs)

    def start(self):
        if self.__is_running is False:
            self.__next_call += self.__interval
            self.__timer = Timer(self.__next_call - time.time(), self._run)
            self.__timer.start()
            self.__is_running = True

    def stop(self):
        self.__timer.cancel()
        self.__timer.join()
        self.__is_running = False
