# syncgit

Sync python dicts, strings ad modules to git repository.


## Example 

```python
import time

from src import Repo, SyncConfig

# This callback is called when changes are pushed to the repo
def update_callback(repo: Repo) -> None:
    print(f"Updated to {repo.commit_hash}")


# Create repo class and import files from repository
rp = Repo("example_repo", "git@github.com:user/example_repo.git", "main")
rp.set_config([
    SyncConfig("about_alice", "json", "alice.json"),
    SyncConfig("about_bob", "yaml", "bob.yml"),
    SyncConfig("text", "text", "text_file.txt"),
    SyncConfig("hello_module", "module", "say_hello.py")
])

# Register call back
rp.set_update_callback(update_callback)

# Start sync
rp.start_sync()

# Imported files will be available as attributes on the repo class
while True:
    time.sleep(1)
    print(rp.about_alice)
    print(rp.about_bob)
    print(rp.text)
    rp.hello_module.say_hello("Alice")

```