from typing import Dict
from typing import List
from typing import Any
from typing import Callable
from typing import Optional
from types import ModuleType

import json
import yaml

from syncgit import _gitcmd as gitcmd
from syncgit._gitcmd import RepoInfo
from syncgit._threadsafe_dict import ThreadSafeDict
from syncgit._threadloop import ThreadLoop
from syncgit._config import SYNCGIT_DEFAULT_POLL_INTERVAL


class UnknownTypeException(Exception):
    pass


class SyncConfig:
    def __init__(self, name: str, sync_type: str, path: str):
        '''
        Parameters
        ----------
            name: str
                Name of the attribute alias
            sync_type : str
                File type. Available options are :code:`"text"` (plain text file, will be converted
                to python string), :code:`"json"`, :code:`"yaml"` (converted to python dict)
                and :code:`"module"` (will be imported the file as python module)
            path: str
                Path to file in the repository
        '''
        self.name = name
        self.type = sync_type
        self.file_path = path


class Repo:
    def __init__(self, name: str, url: str, branch: str) -> None:
        '''
        Parameters
        ----------
        name : str
            Unique name for this repository and branch
        url : str
            Repository URL to sync to (can be ssh or https)
        branch : str
            Name of the branch to sync to
        '''
        self.__repo_info: RepoInfo = RepoInfo(name, url, branch)
        self.__commit_hash = ""
        self.__values: ThreadSafeDict = ThreadSafeDict()
        self.__config: List[SyncConfig]
        self.__update_callback: Optional[Callable[[Any], None]] = None
        self.__thread_loop = ThreadLoop(SYNCGIT_DEFAULT_POLL_INTERVAL, self.__update)

    @property
    def commit_hash(self) -> str:
        '''
        The commit hash of latest sync
        '''
        return self.__commit_hash

    def set_poll_interval(self, seconds: int) -> None:
        '''
        Set polling interval

        Parameters
        ----------
        seconds : int
            Amount of time between synchronization (in seconds, default is 5 seconds)
        '''
        self.__thread_loop.set_interval(seconds)

    def set_update_callback(self, callback: Callable[[Any], None]) -> None:
        '''
        Set callback to be call after synchronization is complete

        Parameters
        ----------
        callback : Callable[[Repo], None]
            This callback will be called when changes are pushed to the repo and
            the new changes have been synchronized. The callback should accept one
            argument, the Repo class
        '''
        self.__update_callback = callback

    def set_config(self, config: List[SyncConfig]) -> None:
        '''
        Configure attributes to sync

        Parameters
        ----------
        config : List[SyncConfig]
            List of SyncConfig specifying attribute names, file path,
            type of the file (see :py:class:`SyncConfig`). These configs will be available
            as class attributes.
        '''
        self.__config = config

    def start_sync(self) -> None:
        '''
        Start sync to git repository
        '''
        self.__thread_loop.start()

    def stop_sync(self) -> None:
        '''
        Stop sync to git repository
        '''
        self.__thread_loop.stop()

    def __pull(self) -> bool:
        new_commit_hash = gitcmd.pull(self.__repo_info)

        if new_commit_hash == self.commit_hash:
            return False

        self.__commit_hash = new_commit_hash
        return True

    def __update(self) -> None:
        if not self.__pull():
            return

        files = self.__get_files()

        for config in self.__config:
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
            file_path_absolute = self.__repo_info.get_abs_path(file_path)

            with open(file_path_absolute) as file:
                files[file_path] = file.read()

        return files

    def __getattr__(self, name: str) -> Any:
        return self.__values[name]
