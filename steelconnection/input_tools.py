# coding: utf-8

"""SteelConnection.input_tools

Convienience functions for getting interactive input from terminal.
"""


from __future__ import print_function
import getpass
import sys


def get_input(prompt=""):
    """Get input in a Python 2/3 compatible way."""
    try:
        data = raw_input(prompt)
    except NameError:
        data = input(prompt)
    finally:
        return data


def get_username(prompt=""):
    return get_input("Enter username: ")


def get_password(prompt=None, password=None):
    """Get password from terminal with discretion."""
    prompt = "Enter password: " if prompt is None else prompt
    while not password:
        verify = False
        while password != verify:
            if verify:
                print("Passwords do not match. Try again", file=sys.stderr)
            password = getpass.getpass(prompt)
            verify = getpass.getpass("Retype password: ")
    return password


def get_password_once(prompt=None):
    """Get password from terminal with discretion."""
    prompt = "Enter password: " if prompt is None else prompt
    return getpass.getpass(prompt)
