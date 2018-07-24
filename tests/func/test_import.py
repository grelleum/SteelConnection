# coding: utf-8


import pytest
import subprocess
import sys
import steelconnection


def test_import_dunder_all():
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
    expected = u'Python version: {0}\nSteelConnection version: {1}\nProject home: {2}\n'.format(
        '.'.join(str(x) for x in sys.version_info[:3]),
        steelconnection.__version__,
        steelconnection.__url__,
    )
    assert repr(output) == repr(expected)
    