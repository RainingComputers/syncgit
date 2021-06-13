# Documentation

## Installation

```
python3 -m pip install syncgit
```

## Class documentation


### class syncgit.SyncConfig(name: str, sync_type: str, path: str)

#### \__init__(name: str, sync_type: str, path: str)

* **Parameters**

    
    * **name** (*str*) – Name of the attribute alias


    * **sync_type** (*str*) – File type. Available options are `"text"` (plain text file),
    `"json"`, `"yaml"` (converted to python dict) and `"module"`
    (will import the file as python module)



### class syncgit.Repo(name: str, url: str, branch: str)

#### \__init__(name: str, url: str, branch: str)

* **Parameters**

    
    * **name** (*str*) – Unique name for this repository and branch


    * **url** (*str*) – Repository URL to sync to (can be ssh or https)


    * **branch** (*str*) – Name of the branch to sync to



#### set_config(config: List[syncgit._repo.SyncConfig])
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



#### commit_hash()
The commit hash of latest sync
