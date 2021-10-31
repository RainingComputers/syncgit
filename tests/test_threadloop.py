import time

from syncgit._threadloop import ThreadLoop


class CallIntervalAssertMock:
    def __init__(self) -> None:
        self._call_count = 0
        self._last_time = 0.0
        self._accumulated_time_diff = 0.0

    def __call__(self) -> None:
        if self._call_count == 0:
            self._last_time = time.time()
        else:
            current_time = time.time()
            self._accumulated_time_diff += current_time - self._last_time
            self._last_time = current_time

        self._call_count += 1

    @property
    def avg_interval(self) -> float:
        return self._accumulated_time_diff / (self._call_count - 1)

    @property
    def call_count(self) -> int:
        return self._call_count


def test_threadloop() -> None:
    callback = CallIntervalAssertMock()
    threadloop = ThreadLoop(1, callback)
    threadloop.start()
    time.sleep(2)
    threadloop.stop()

    assert callback.call_count >= 3 and callback.call_count <= 4
    assert int(callback.avg_interval) == 1
