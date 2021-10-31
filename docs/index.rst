syncgit
=======

Sync python dicts, strings and modules to files in git repository.

NOTE: syncgit calls git using subprocess, setup git so it does not ask for username or password, otherwise you will get a timeout exception.

Installation
------------

.. code-block:: bash

   python3 -m pip install syncgit


Class documentation
-------------------


.. autoclass:: syncgit.SyncConfig

   .. automethod:: __init__


.. autoclass:: syncgit.Repo

   .. automethod:: __init__

   .. automethod:: set_config

   .. automethod:: start_sync

   .. automethod:: stop_sync

   .. automethod:: sync
   
   .. automethod:: set_poll_interval
   
   .. automethod:: set_update_callback
   
   .. autoattribute:: commit_hash

Example
-------

**Example repo**

.. code-block::

    syncgit-test
    ├── alice.json
    │   └── {
    │           "name": "Alice",
    │           "age": 24,
    │           "interests": [
    │               "Programming",
    │               "Skiing"
    │           ]
    │       }
    ├── bob.yml
    │   └── name: Bob
    │       age: 22
    │       interests:
    │         - Reading
    │         - Drawing
    ├── say_hello.py
    │   └── def say_hello(name): 
    │           print(f"Hello {name}, nice to meet you")
    └── text_file.txt
        └── This is a text file

**Code**

.. code-block:: python

   from typing import List
   
   import time
   
   from syncgit import Repo, SyncConfig
   
   # This callback is called when changes are pushed to the repo
   def update_callback(repo: Repo, changes: List[SyncConfig]) -> None:
       print(f"Updated to commit {repo.commit_hash}")
   
       for change in changes:
           print(f"Updated {change.name}")
   
   # Create repo class and import files from repository
   rp = Repo("example_repo", "git@github.com:RainingComputers/syncgit-test.git", "main")
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
   # Changes are reflected immediately on these attributes real time
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

Environment Variables
---------------------

.. list-table::
   :header-rows: 1

   * - Name
     - Description
     - Default

   * - SYNCGIT_CMD_TIMEOUT
     - Timeout for pulling changes from repository
     - 15

   * - SYNCGIT_REPOS_DIR_NAME
     - Directory to store all synced repositories
     - .repos

   * - SYNCGIT_DEFAULT_POLL_INTERVAL
     - Default polling interval to pull changes and sync
     - 5
