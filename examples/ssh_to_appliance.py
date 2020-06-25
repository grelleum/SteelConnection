#!/usr/bin/env python3

# coding: utf-8

#         ______          __
#        / __/ /____ ___ / /
#    ____\ \/ __/ -_) -_) /      __  _
#   / _____/\__/\__/\__/_/_ ____/ /_(_)__  ___
#  / /__/ _ \/ _ \/ _ \/ -_) __/ __/ / _ \/ _ \
#  \___/\___/_//_/_//_/\__/\__/\__/_/\___/_//_/
#
# SteelConnection
# Simplify access to the Riverbed SteelConnect CX REST API.
#
# https://pypi.org/project/steelconnection
# https://github.com/grelleum/SteelConnection


"""
SSH to SteelConnect CX appliances and run commands.
Uses Paramiko for SSH access.

Written using 'f-strings' for Python 3.6 or higher.
"""


import paramiko
import steelconnection


REALM = "myrealm.riverbed.cc"

appliances = [
    "XN1111111AAAAAAA",
    "XN2222222BBBBBBB",
]

commands = ["ip -4 a", "lpm routes"]


def main():
    """SSH to appliances and run commands."""

    sc = steelconnection.SConnect(REALM)

    for appliance in appliances:

        # Get node ID ffrom serial number.
        node_id = sc.lookup.node(appliance)

        # Start reverse SSH tunnel from appliance to SCM.
        tunnel = sc.sshtunnel(node_id)

        # Setup proxy command for Paramiko
        hostname = f"{appliance}.{REALM}"
        proxy_command = f"nc -X connect -x {REALM}:3903 {hostname} 22"

        # Create a scoket for the proxied connection.
        sock = paramiko.proxy.ProxyCommand(proxy_command)

        # Create paramiko client.
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Make SSH connection to appliance.
        client.connect(hostname=hostname, username="root", sock=sock)

        # Execute the commands
        for command in commands:
            sdtin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode()
            print(f"# Output of '{command}'")
            print(output)

        # close the connection:
        client.close()


if __name__ == "__main__":
    main()

