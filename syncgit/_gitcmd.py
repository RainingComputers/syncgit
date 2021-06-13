import subprocess
import os
import shutil

from typing import List

from syncgit._config import SYNCGIT_CMD_TIMEOUT, SYNCGIT_REPO_DIR_NAME


def _exec_cmd(command: List[str]) -> None:
    subprocess.run(command, timeout=SYNCGIT_CMD_TIMEOUT,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)


def _exec_cmd_str(command: List[str]) -> str:
    subp = subprocess.run(command, timeout=SYNCGIT_CMD_TIMEOUT,
                          stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=True)
    return subp.stdout.decode('utf-8')


def _get_repo_dir(local_name: str) -> str:
    return f"./{SYNCGIT_REPO_DIR_NAME}/{local_name}"


def _git(local_name: str) -> List[str]:
    return ["git", "-C", _get_repo_dir(local_name)]


def _create_repo_dir(local_name: str, url: str) -> None:
    repo_dir = _get_repo_dir(local_name)

    if os.path.exists(repo_dir):
        return

    os.makedirs(repo_dir)
    _exec_cmd(_git(local_name) + ["init"])
    _exec_cmd(_git(local_name) + ["remote", "add", "origin", url])


def commit_hash(local_name: str) -> str:
    return _exec_cmd_str(_git(local_name) + ["show", "-s", "--format=%H"]).rstrip()


def pull(local_name: str, url: str, branch: str = "main") -> str:
    _create_repo_dir(local_name, url)

    _exec_cmd(_git(local_name) + ["pull", "origin", branch])

    return commit_hash(local_name)


def remove(local_name: str) -> None:
    shutil.rmtree(_get_repo_dir(local_name))


def remove_all() -> None:
    shutil.rmtree(f"./{SYNCGIT_REPO_DIR_NAME}")
