# coding: utf-8


import pytest
import subprocess
import steelconnection


def test_import_dumder_all():
    expected = set((
        'SConAPI', 'SConWithoutExceptions', 'SConExitOnError',
        'AuthenticationError', 'APINotEnabled', 
        'BadRequest', 'InvalidResource', 
        'get_input', 'get_username', 'get_password',
    ))
    set(steelconnection.__all__) == expected


def test_import_on_command_line():
    output = subprocess.check_output('python -m steelconnection', shell=True)
    output = output.decode()
    expected = u'SteelConnection version: {0}\nProject home: {1}\n'.format(
        steelconnection.__version__,
        steelconnection.__url__,
    )
    assert repr(output) == repr(expected)
    