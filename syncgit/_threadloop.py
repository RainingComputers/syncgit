from typing import Any
from threading import Thread

import time


class ThreadLoop:
    def __init__(self, interval: int, callback: Any) -> None:
        self.__interval = interval
        self.__callback = callback
        self.__running = False
        self.__thread: Thread

    def start(self) -> None:
        self.__callback()
        self.__running = True
        self.__thread = Thread(target=self.__loop)
        self.__thread.setDaemon(True)
        self.__thread.start()

    def stop(self) -> None:
        self.__running = False
        self.__thread.join()

    def set_interval(self, seconds: int) -> None:
        self.__interval = seconds

    def __loop(self) -> None:
        starttime = time.time()

        while self.__running:
            time.sleep(self.__interval - ((time.time() - starttime) % self.__interval))
            self.__callback()
