Documentation
=============

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
   
   .. automethod:: set_poll_interval
   
   .. automethod:: set_update_callback
   
   .. autoattribute:: commit_hash
