Logging
=======

Real-time logging can be enabled by placing the following code near the top
of your script.

.. code:: python

   import logging

   logging.basicConfig(level=logging.DEBUG)
   logger = logging.getLogger(__name__)

This will provide details on what has been sent to and received from the
SteelConnect manager.
