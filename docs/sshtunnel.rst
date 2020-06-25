sshtunnel
=========

The sshtunnel method provides an easy way to start, stop, or restart
a reverse SSH tunnel.

.. code:: python

   <object>.sshtunnel(node_id, timeout=15, restart=False, stop=False)


Examples:

.. code:: python

   # Start ssh tunnel.  Wait as long as 15 seconds for tunnel to establish.
   result = <object>.sshtunnel(node_id)

   # Start ssh tunnel.  Increase timeout to 30 seconds for tunnel to establish.
   result = <object>.sshtunnel(node_id, timeout=30)

   # Stop an existing ssh tunnel.
   result = <object>.sshtunnel(node_id, stop=True)

   # Stop an existing ssh tunnel and re-establish tunnel.
   result = <object>.sshtunnel(node_id, restart=True)

Returns a dictionary object with the state of the tunnel, or an empty dictionary if ``stop=True``.