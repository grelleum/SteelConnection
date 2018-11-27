# coding: utf-8

"""
Provide functions to sinplify virtual image build and download.

To be called from SteelConnection main object classes.
Not supported for direct use.
"""

from __future__ import print_function
import locale
import os
import sys
import time

from .exceptions import ResourceGone


def _no_op(*args, **kwargs):
    """No operation."""
    return None


def _print_flush(*args, **kwargs):
    """
    Print with flush to allow Python 2 compatibility.

    Args:
        *args: Optional arguments that ``print`` accepts.
        **kwargs: Optional arguments that ``print`` accepts.

    Returns:
        None
    """
    print(*args, **kwargs)
    sys.stdout.flush()


def _download_image(sconnect, nodeid, save_as=None, build=None, quiet=False):
    r"""
    Download image and save to file.

    Args:
        sconnect (str): SteelConnection object.
        nodeid (str): The node id of the appliance.
        save_as (str): The file path to download the image.
        build (str): Target hypervisor for image.
        quiet (bool): Disable update printing when true.

    Returns:
        dict: Object indication the success fo the operation.
    """
    verbose = _no_op if quiet else _print_flush
    if build:
        _prepare_image(sconnect, nodeid, build, verbose)
    status = _wait_for_ready(sconnect, nodeid, verbose)
    if status is None:
        raise ValueError("\n'build' not specified and no image available.")
    source_file = status["image_file"]
    verbose("\nImage file '{}' available for download.".format(source_file))
    save_as = _get_file_path(source_file, save_as)
    _stream_download(sconnect, nodeid, source_file, save_as, verbose)
    if sconnect.response.ok:
        locale.setlocale(locale.LC_ALL, "")
        filesize = locale.format("%d", os.stat(save_as).st_size, grouping=True)
        return {"filename": save_as, "filesize": "{} bytes".format(filesize)}


def _prepare_image(sconnect, nodeid, build, verbose):
    """
    Request an image build from SCM.

    Args:
        sconnect (str): SteelConnection object.
        nodeid (str): The node id of the appliance.
        build (str): Type of hypervisor for image.
        verbose (function): The function used for prining.

    Returns:
        None
    """
    verbose("Requesting image of type " + build, end=": ")
    sconnect.post("/node/{}/prepare_image".format(nodeid), data={"type": build})
    # In case there is no config for the appliance, the build will fail.
    # Checking the status when build fails will result in error 500.
    # Checking immediately, the explanation will have no error reason.
    # By delaying after the build, we can get correct error on check.
    time.sleep(0.5)
    verbose("Done.")


def _wait_for_ready(sconnect, nodeid, verbose, retries=600, sleep_time=1):
    """
    Check status periodically until file is ready.

    Args:
        sconnect (str): SteelConnection object.
        nodeid (str): The node id of the appliance.
        verbose (function): The function used for prining.
        retries (int): Number of times to check status before giving up.
        build (int or float): Pause interval between status checks.

    Returns:
        dict or None
    """
    for _ in range(retries):
        verbose(".", end="")
        try:
            status = sconnect.get("/node/{}/image_status".format(nodeid))
        except ResourceGone:
            return None
        else:
            if status.get("status", False):
                return status
        time.sleep(sleep_time)
    else:
        raise RuntimeError("Timed out waiting for image ready.")


def _get_file_path(source_file, save_as):
    """
    Get file name and determine destination file path.

    Args:
        source_file (str): Name of the source file to download.
        save_as (str): Filepath where file is written.

    Returns:
        str: Path and filename.
    """
    if save_as is None:
        save_as = source_file
    if os.path.isdir(save_as):
        save_as = os.path.join(save_as, source_file)
    return save_as


def _stream_download(sconnect, nodeid, source_file, save_as, verbose):
    """
    Save stream of binary data to disk.

    Args:
        sconnect (str): SteelConnection object.
        nodeid (str): The node id of the appliance.
        source_file (str): Name of the source file to download.
        save_as (str): Filepath where file is written.
        verbose (function): The function used for prining.

    Returns:
        None
    """
    verbose("Downloading file as '{}'".format(save_as), end=" ")
    with open(save_as, "wb") as fd:
        chunks = sconnect.stream(
            "/node/{}/get_image".format(nodeid), params={"file": source_file}
        )
        for index, chunk in enumerate(chunks):
            fd.write(chunk)
            if index % 50 == 0:
                verbose(".", end="")
    verbose("\nDownload complete.")
