Virtual Appliance Image Download
================================

download_image
--------------

There is a convenience method ``.download_image`` that can be used to
download a virtual appliance image file. This method will optionally
request the ‘build’ of a virtual appliance image, when you set
``build=`` a vm type, such as ``build=kvm`` or ``build=ova``. Then it
will check the availability of the image file every one second until the
file is found. Next it will download the file to the location specifed
by the ``save_as=`` parameter. ``download_image`` will print status
messages while checking the status and downloading the file. To disable
status messages, include the ``quiet=True`` parameter. Here are some
examples:

.. code:: python

   # Build kvm image and specify the downloads folder and filename.
   sc.download_image(node['id'], save_as='Downloads/scon_vgw.zip', build='kvm')

   # Build a hyperv image and download to the current directory using the default file name.
   sc.download_image(node['id'], build='hyperv')

   # Download an existing image to /images/ directory and suppress status updates.
   sc.download_image(node['id'], save_as='/images/scon_vgw.zip', quiet=True)


Other Binary Data
-----------------

In the event another API call returns binary data, You can access it
directly through the object’s ‘.response.content’ attribute, or by
calling the ‘.savefile(filename)’ method, which will save the binary
data to a file.
