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

The code above will display logging to standard output (the screen).
Here is alternative code that can be used to log to a file:

.. code:: python

   import logging

   logging.basicConfig(
       level=logging.DEBUG,
       format="%(asctime)s [%(name)s.%(levelname)s]: %(message)s",
       filename='steelog.txt',
   )
   logger = logging.getLogger(__name__)

The inclusion of the `filename` parameter, sends it to a file, while the
`format` parameter adds a timestamp to each logged message.
