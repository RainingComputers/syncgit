# syncgit

Sync python dicts, strings and modules to files in git repository.

NOTE: syncgit calls git using subprocess, setup git so it does not ask for username or password,
otherwise you will get a timeout exception.

### Installation

```
python -m pip install syncgit
```

### Documentation

https://syncgit.readthedocs.io/en/latest/

### Example 

```python
from typing import List

import time

from syncgit import Repo, SyncConfig

# This callback is called when changes are pushed to the repo
def update_callback(repo: Repo, changes: List[SyncConfig]) -> None:
    print(f"Updated to commit {repo.commit_hash}")

    for change in changes:
        print(f"Updated {change.name}")

# Create repo class and import files from repository
rp = Repo("example_repo", "git@github.com:user/example_repo.git", "main")
rp.set_config([
    SyncConfig("about_alice", "alice.json", "json"),
    SyncConfig("about_bob", "bob.yml"),
    SyncConfig("text", "text_file.txt", "text"),
    SyncConfig("hello_module", "say_hello.py")
])

# Register call back
rp.set_update_callback(update_callback)

# Start sync
rp.start_sync()

# Imported files will be available as attributes on the repo class
try:
    while True:
        time.sleep(1)
        print(rp.about_alice)
        print(rp.about_bob)
        print(rp.text)
        rp.hello_module.say_hello("Alice")
except KeyboardInterrupt:
    print("Stopping sync")
    rp.stop_sync()

```
