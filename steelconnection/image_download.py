# coding: utf-8

"""SteelConnection image.

Convienience functions for virtual machine image downloads.
To be called from SteelConnection main object classes.
Not supported for direct use.
"""

from __future__ import print_function

import locale
import os
import time

from .exceptions import ResourceGone


def silence(*args, **kwargs):
    pass


def _download_image(sconnect, nodeid, save_as=None, build=None, quiet=False):
    r"""Download image and save to file.

    :param str sconnect: SteelConnection object.
    :param str nodeid: The node id of the appliance.
    :param str save_as: The file path to download the image.
    :param str build: Target hypervisor for image.
    :param bool quiet: Disable update printing when true.
    """
    qprint = silence if quiet else print
    if build:
        _prepare_image(sconnect, nodeid, build, qprint)
    status = _wait_for_ready(sconnect, nodeid, qprint)
    if status is None:
        raise ValueError("'build' not specified and no image available.")
    source_file = status['image_file']
    qprint("Image file '{}' available for download".format(source_file))
    save_as = _get_file_path(source_file, save_as)
    _stream_download(sconnect, nodeid, source_file, save_as, qprint)
    if sconnect.response.ok:
        locale.setlocale(locale.LC_ALL, '')
        filesize = locale.format('%d', os.stat(save_as).st_size, grouping=True)
        return {
            'filename': save_as,
            'filesize': '{} bytes'.format(filesize),
        }


def _prepare_image(sconnect, nodeid, build, qprint):
    """Check status every second until file is ready."""
    qprint('Requesting image of type ' + build, end=':', flush=True)
    sconnect.post(
        '/node/{}/prepare_image'.format(nodeid),
        data={'type': build}
    )
    qprint('Done.')


def _wait_for_ready(sconnect, nodeid, qprint):
    """Check status every second until file is ready."""
    qprint('Checking availability of image', end=' ', flush=True)
    while True:
        qprint('.', end='', flush=True)
        try:
            status = sconnect.get('/node/{}/image_status'.format(nodeid))
        except ResourceGone:
            return None
        else:
            if status.get('status', False):
                return status
        time.sleep(1)


def _get_file_path(source_file, save_as):
    """Get file name and determine destination file path."""
    if save_as is None:
        save_as = source_file
    if os.path.isdir(save_as):
        save_as = os.path.join(save_as, source_file)
    return save_as


def _stream_download(sconnect, nodeid, source_file, save_as, qprint):
    qprint('\nDownloading file as', save_as, end=' ', flush=True)
    with open(save_as, 'wb') as fd:
        chunks = sconnect.stream(
            '/node/{}/get_image'.format(nodeid),
            params={'file': source_file},
        )
        for index, chunk in enumerate(chunks):
            fd.write(chunk)
            if index % 50 == 0:
                qprint('.', end='', flush=True)
    qprint('\nDownload complete.')
