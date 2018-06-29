# coding: utf-8

import getpass
import sys
from steelconnection import input_tools


def test_get_input(monkeypatch):
    if sys.version_info.major < 3:
        monkeypatch.setattr('__builtin__.raw_input', lambda x: 'SteelConnect')
    else:
        monkeypatch.setattr('builtins.input', lambda x: 'SteelConnect')
    name = input_tools.get_input()
    assert name == 'SteelConnect'


def test_get_username(monkeypatch):
    if sys.version_info.major < 3:
        monkeypatch.setattr('__builtin__.raw_input', lambda x: 'SteelConnect')
    else:
        monkeypatch.setattr('builtins.input', lambda x: 'SteelConnect')
    name = input_tools.get_username()
    assert name == 'SteelConnect'


def test_get_password(monkeypatch):
    monkeypatch.setattr('getpass.getpass', lambda x: 'mypassword')
    password = input_tools.get_password()
    assert password == 'mypassword'


def test_get_password_once(monkeypatch):
    monkeypatch.setattr('getpass.getpass', lambda x: 'mypassword')
    password = input_tools.get_password_once()
    assert password == 'mypassword'
