# pylint: disable=protected-access

import os
from typing import List

import filecmp

from unittest.mock import Mock

from pytest import MonkeyPatch

import syncgit
import syncgit._gitcmd
from syncgit import SyncConfig, Repo
from syncgit._gitcmd import RepoInfo


class SyncConfigFake(SyncConfig):
    def __init__(self, name: str, path: str, sync_type: str = "auto") -> None:
        self.fake_hash = "abcd"
        super().__init__(name, path, sync_type=sync_type)

    @property
    def file_path(self) -> str:
        return os.path.join(self.fake_hash, super().file_path)


class GitcmdPullStub:
    def __init__(self) -> None:
        self.fake_hash = "abcd"

    def __call__(self, _: RepoInfo) -> str:
        return self.fake_hash


class GitcmdChangesStub:
    def __init__(self) -> None:
        self.__previous_hash = "abcd"
        self.__fake_hash = "abcd"

    @property
    def fake_hash(self) -> str:
        return self.__fake_hash

    @fake_hash.setter
    def fake_hash(self, new_fake_hash: str) -> None:
        self.__previous_hash = self.__fake_hash
        self.__fake_hash = new_fake_hash

    def get_changes(self, repo_info: RepoInfo) -> List[str]:
        changes: List[str] = []

        old_dir = os.path.join(repo_info.dir, self.__previous_hash)
        new_dir = os.path.join(repo_info.dir, self.__fake_hash)

        for file in os.listdir(old_dir):
            if not filecmp.cmp(os.path.join(old_dir, file), os.path.join(new_dir, file)):
                changes.append(os.path.join(self.__fake_hash, file))

        return changes

    def __call__(self, repo_info: RepoInfo) -> List[str]:
        if self.__previous_hash == self.__fake_hash:
            return []

        return self.get_changes(repo_info)


def set_fake_hash(fake_hash: str, fake_test_config: List[SyncConfigFake],
                  pull_stub: GitcmdPullStub, changes_stub: GitcmdChangesStub) -> None:
    for cfg in fake_test_config:
        cfg.fake_hash = fake_hash

    pull_stub.fake_hash = fake_hash
    changes_stub.fake_hash = fake_hash


def test_repo(monkeypatch: MonkeyPatch) -> None:
    update_callback = Mock()
    gitcmd_pull_stub = GitcmdPullStub()
    gitcmd_changes_stub = GitcmdChangesStub()

    monkeypatch.setattr(syncgit._gitcmd, "pull", gitcmd_pull_stub)
    monkeypatch.setattr(syncgit._gitcmd, "changes", gitcmd_changes_stub)
    monkeypatch.setattr(syncgit._gitcmd, "_create_repo_dir", Mock())

    repo = Repo("fake_repo", "git@github.com:user/fake_repo.git", "main")

    fake_test_config = [
        SyncConfigFake("about_alice", "alice.json", "json"),
        SyncConfigFake("about_bob", "bob.yml"),
        SyncConfigFake("text", "text_file.txt", "text"),
        SyncConfigFake("hello_module", "say_hello.py")
    ]

    repo.set_config(fake_test_config)  # type: ignore

    repo.set_update_callback(update_callback)

    repo.sync()

    assert repo.about_alice == {"name": "Alice", "age": 22, "interests": ["Programming", "Skiing"]}
    assert repo.about_bob == {"name": "Bob", "age": 22, "interests": ["Reading", "Drawing"]}
    assert repo.text == "This is a text file"
    assert repo.hello_module.say_hello("bob") == "Hello bob, nice to meet you"

    set_fake_hash("efgh", fake_test_config, gitcmd_pull_stub, gitcmd_changes_stub)
    repo.sync()

    assert repo.about_alice == {"name": "Alice", "age": 24, "interests": ["Programming", "Manga"]}
    assert repo.about_bob == {"name": "Bob", "age": 24, "interests": ["Programming", "Drawing"]}
    assert repo.text == "This is a text file"
    assert repo.hello_module.say_hello("bob") == "Hello bob, nice to meet you"
