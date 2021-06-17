from typing import Dict
from typing import Any

from threading import Lock


class ThreadSafeDict:
    def __init__(self) -> None:
        self.__values: Dict[str, Any] = {}
        self.__locks: Dict[str, Lock] = {}

    def __upsert_lock(self, key: str) -> Lock:
        try:
            lock = self.__locks[key]
        except KeyError:
            lock = Lock()
            self.__locks[key] = lock

        return lock

    def __setitem__(self, key: str, value: Any) -> Any:
        with self.__upsert_lock(key):
            self.__values[key] = value

    def __getitem__(self, key: str) -> Any:
        with self.__locks[key]:
            return self.__values[key]

    def __len__(self) -> int:
        return len(self.__values)
