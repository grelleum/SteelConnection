# coding: utf-8

"""SteelConnection image.

Convienience objects for virtual machin image downloads.
To be called from SteelConnection main object classes.
Not supported for direct use.
"""

from __future__ import print_function

import os
import time
import warnings

from .__version__ import __version__
from .exceptions import AuthenticationError, APINotEnabled
from .exceptions import BadRequest, ResourceGone, InvalidResource


def quiet_print(quiet):
    if quiet:
        return silence
    else:
        return print


def silence(*args, **kwargs):
    pass


def _download_image(sconnection, nodeid, save_as=None, build=None, quiet=False):
    r"""Download image and save to file.
    :param str sconnection: SteelConnection object.
    :param str nodeid: The node id of the appliance.
    :param str save_as: The file path to download the image.
    :param str build: Target hypervisor for image.
    :param bool quiet: Disable update printing when true.
    """
    qprint = quiet_print(quiet)
    if build:
        _prepare_image(sconnection, nodeid, build, qprint)
    status = _wait_for_ready(sconnection, nodeid, qprint)
    if status is None:
        raise ValueError("'build' not specified and no image available.")
    source_file = status['image_file']
    save_as = _get_file_path(source_file, save_as)
    _stream_download(sconnection, nodeid, source_file, save_as, qprint)
    return sconnection.response.ok


def _prepare_image(sconnection, nodeid, build, qprint):
    """Check status every second until file is ready."""
    qprint('Requesting image of type ' + build)
    sconnection.post(
        '/node/{}/prepare_image'.format(nodeid),
        data={'type': build}
    )


def _check_status(sconnection, nodeid, qprint):
    """Check status every second until file is ready."""
    qprint('Checking if image file is available')


def _wait_for_ready(sconnection, nodeid, qprint):
    """Check status every second until file is ready."""
    qprint('Checking availability of image', end=' ', flush=True)
    while True:
        qprint('.', end='', flush=True)
        try:
            status = sconnection.get('/node/{}/image_status'.format(nodeid))
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


def _stream_download(sconnection, nodeid, source_file, save_as, qprint):
    qprint('\nDownloading file as', save_as, end=' ', flush=True)
    with open(save_as, 'wb') as fd:
        for index, chunk in enumerate(
                sconnection.stream(
                    '/node/{}/get_image'.format(nodeid),
                    params={'file': source_file},
                )
            ):
            fd.write(chunk)
            if not index % 50:
                qprint('.', end='', flush=True)
    qprint('\nDownload complete.')
