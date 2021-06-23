import subprocess
import os
import shutil
from contextlib import suppress

from typing import List
from typing import Optional

from syncgit._config import SYNCGIT_CMD_TIMEOUT, SYNCGIT_REPO_DIR_NAME


class RepoInfo:
    def __init__(self, local_name: str, url: str, branch: str, dir_path: Optional[str]) -> None:
        self.local_name = local_name
        self.url = url
        self.branch = branch

        if dir_path is None:
            self.dir = os.path.join(SYNCGIT_REPO_DIR_NAME, self.local_name)
        else:
            self.dir = dir_path

    def get_abs_path(self, file_name: str) -> str:
        return os.path.join(self.dir, file_name)


def _exec_cmd(command: List[str]) -> None:
    subprocess.run(command, timeout=SYNCGIT_CMD_TIMEOUT,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)


def _exec_cmd_str(command: List[str]) -> str:
    subp = subprocess.run(command, timeout=SYNCGIT_CMD_TIMEOUT,
                          stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=True)

    return subp.stdout.decode('utf-8')


def _git(repo_info: RepoInfo) -> List[str]:
    return ["git", "-C", repo_info.dir]


def _create_repo_dir(repo_info: RepoInfo) -> None:
    if os.path.exists(repo_info.dir):
        return

    os.makedirs(repo_info.dir)
    _exec_cmd(_git(repo_info) + ["init"])
    _exec_cmd(_git(repo_info) + ["remote", "add", "origin", repo_info.url])


def commit_hash(repo_info: RepoInfo) -> str:
    return _exec_cmd_str(_git(repo_info) + ["show", "-s", "--format=%H"]).rstrip()


def pull(repo_info: RepoInfo) -> str:
    _create_repo_dir(repo_info)

    with suppress(subprocess.SubprocessError):
        _exec_cmd(_git(repo_info) + ["pull", "origin", repo_info.branch])

    return commit_hash(repo_info)


def changes(repo_info: RepoInfo) -> List[str]:
    return _exec_cmd_str(_git(repo_info) + ["diff", "--name-only", "HEAD^", "HEAD"]).splitlines()


def remove(repo_info: RepoInfo) -> None:
    shutil.rmtree(repo_info.dir)


def remove_all() -> None:
    shutil.rmtree(f"./{SYNCGIT_REPO_DIR_NAME}")
