from typing import Dict
from typing import List
from typing import Any
from typing import Callable
from typing import Optional
from types import ModuleType

import time
import os
import json
from collections import namedtuple
from threading import Lock, Thread

import yaml

from src import _gitcmd as gitcmd
from src._exceptions import UnknownTypeException
from src._config import SYNCGIT_POLL_INTERVAL


SyncConfig = namedtuple("SyncConfig", "name type file_path")


class Repo:
    def __init__(self, name: str, url: str, branch: str) -> None:
        self.__local_name = name
        self.__url = url
        self.__branch = branch
        self.__values: Dict[str, Any] = {}
        self.__lock = Lock()
        self.__config: List[SyncConfig]
        self.__current_hash: str = ""
        self.__update_callback: Optional[Callable[[Any], None]] = None

    @property
    def commit_hash(self) -> str:
        return self.__current_hash

    def set_update_callback(self, callback: Callable[[Any], None]) -> None:
        self.__update_callback = callback

    def start_sync(self) -> None:
        self.__update()
        poll_thread = Thread(target=self.__poll_loop)
        poll_thread.setDaemon(True)
        poll_thread.start()

    def __pull(self) -> str:
        return gitcmd.pull(self.__local_name, self.__url, self.__branch)

    def __poll_loop(self) -> None:
        starttime = time.time()

        while True:
            self.__update()
            time.sleep(SYNCGIT_POLL_INTERVAL - ((time.time() - starttime) % SYNCGIT_POLL_INTERVAL))

    def set_config(self, config: List[SyncConfig]) -> None:
        self.__config = config

    def __update(self) -> None:
        new_hash = self.__pull()

        if new_hash == self.__current_hash:
            return

        self.__current_hash = new_hash

        files = self.__get_files()

        for config in self.__config:
            with self.__lock:
                self.__set_value(config, files[config.file_path])

        if self.__update_callback is not None:
            self.__update_callback(self)

    def __set_value(self, config: SyncConfig, str_value: str) -> None:
        if config.type == "text":
            self.__values[config.name] = str_value
        elif config.type == "json":
            self.__values[config.name] = json.loads(str_value)
        elif config.type == "yaml":
            self.__values[config.name] = yaml.safe_load(str_value)
        elif config.type == "module":
            self.__set_module(config.name, str_value)
        else:
            raise UnknownTypeException

    def __set_module(self, name: str, str_src: str) -> None:
        compiled = compile(str_src, '', 'exec')
        module = ModuleType(name)
        exec(compiled, module.__dict__)  # pylint: disable=exec-used
        self.__values[name] = module

    def __get_files(self) -> Dict[str, str]:
        files: Dict[str, str] = {}

        for config in self.__config:
            file_path = config.file_path
            file_path_absolute = os.path.join(gitcmd.SYNCGIT_REPO_DIR_NAME, self.__local_name, file_path)

            with open(file_path_absolute) as file:
                files[file_path] = file.read()

        return files

    def __getattr__(self, name: str) -> Any:
        return self.__values[name]
