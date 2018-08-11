# coding: utf-8

"""
test_get_ports.py

Pytest functions intended to validate the examples/get_ports.py
This relies on a environment variables to complete.
"""

import os
import sys


username = os.environ.get('SCONUSER')
password = os.environ.get('SCONPASSWD')
realm = os.environ.get('SCONREALM')
org_name = os.environ.get('SCONORG')
appliance = os.environ.get('SCONAPPLIANCE')


def provide_input(prompt, words=[realm, username, appliance]):
    return words.pop(0)


def test_get_ports(capsys, monkeypatch):

    if sys.version_info.major < 3:
        monkeypatch.setattr('__builtin__.raw_input', provide_input)
    else:
        monkeypatch.setattr('builtins.input', provide_input)
    monkeypatch.setattr('getpass.getpass', lambda x: password)
    import get_ports
    get_ports.main()
    captured = capsys.readouterr()
    assert not captured.err
    assert 'YOGI_LAN1' in captured.out
    assert 'eth0' in captured.out
    assert 'UP' in captured.out or 'DOWN' in captured.out
