# coding: utf-8


import subprocess
import sys
import steelconnection


def test_import_dunder_all():
    expected = set(
        (
            "SConnect",
            "SConWithoutExceptions",
            "SConExitOnError",
            "AuthenticationError",
            "APINotEnabled",
            "BadRequest",
            "InvalidResource",
            "get_input",
            "get_username",
            "get_password",
        )
    )
    set(steelconnection.__all__) == expected


def test_import_on_command_line():
    output = subprocess.check_output("python -m steelconnection", shell=True)
    output = output.decode()
    lines = [
        steelconnection.ASCII_ART,
        "Python version: " + ".".join(str(x) for x in sys.version_info[:3]),
        "SteelConnection version: " + steelconnection.version,
        "Documentation: " + steelconnection.about.documentation,
        "Project home:  " + steelconnection.about.project_home,
    ]
    expected = u"\n".join(lines) + "\n\n"
    assert repr(output) == repr(expected)
