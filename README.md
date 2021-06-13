# syncgit

Sync python dicts, strings and modules to files in git repository.

NOTE: syncgit calls git using subprocess, setup git so it does not ask for username or password,
otherwise you will get a timeout exception.


### Example 

```python
import time

from syncgit import Repo, SyncConfig

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

## Class documentation


### class syncgit.SyncConfig(name: str, sync_type: str, path: str)

#### \__init__(name: str, sync_type: str, path: str)

* **Parameters**

    
    * **name** (*str*) – Name of the attribute alias


    * **sync_type** (*str*) – File type. Available options are `"text"` (plain text file, will be converted
    to python string), `"json"`, `"yaml"` (converted to python dict)
    and `"module"` (will be imported the file as python module)


    * **path** (*str*) – Path to file in the repository.



### class syncgit.Repo(name: str, url: str, branch: str)

#### \__init__(name: str, url: str, branch: str)

* **Parameters**

    
    * **name** (*str*) – Unique name for this repository and branch


    * **url** (*str*) – Repository URL to sync to (can be ssh or https)


    * **branch** (*str*) – Name of the branch to sync to



#### set_config(config: List[syncgit.SyncConfig])
Configure attributes to sync


* **Parameters**

    **config** (*List**[**SyncConfig**]*) – List of SyncConfig specifying attribute names, file path,
    type of the file (see `SyncConfig`). These configs will be available as class attributes.



#### start_sync()
Start sync to git repository


#### set_poll_interval(seconds: int)
Set polling interval


* **Parameters**

    **seconds** (*int*) – Amount of time between synchronization (in seconds)



#### set_update_callback(callback: Callable[[Any], None])
Set callback to be call after synchronization is complete


* **Parameters**

    **callback** (*Callable**[**[**Repo**]**, **None**]*) – This callback will be called when changes are pushed to the repo and
    the new changes have been synchronized. The callback should accept one
    argument, the Repo class



#### commit_hash
The commit hash of latest sync
