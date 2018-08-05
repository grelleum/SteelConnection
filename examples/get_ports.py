
# coding: utf-8

#    ______          _______                       __  _
#   / __/ /____ ___ / / ___/__  ___  ___  ___ ____/ /_(_)__  ___
#  _\ \/ __/ -_) -_) / /__/ _ \/ _ \/ _ \/ -_) __/ __/ / _ \/ _ \
# /___/\__/\__/\__/_/\___/\___/_//_/_//_/\__/\__/\__/_/\___/_//_/
#
#
# SteelConnection
# Simplify access to the Riverbed SteelConnect REST API.
#
# https://pypi.org/project/steelconnection
# https://github.com/grelleum/SteelConnection

"""List port information for a SteelConnect appliance."""

from __future__ import print_function

import steelconnection


def main():
    sc = steelconnection.SConnect()

    appliance = steelconnection.get_input('Enter appliance serial number: ')
    node = sc.lookup.node(appliance)

    ports = sc.get('node/' + node['id'] + '/ports')

    line = '{:14}{:10}{:8}{:8}{:8}'
    print(line.format('\nPort ID', 'ifname', 'Link', 'Speed', 'Duplex'))
    print(line.format('-------', '------', '----', '-----', '------'))

    for port in ports:
        resource = 'port/{}'.format(port['id'])
        port_status = sc.getstatus(resource)
        print(line.format(
            port['port_id'],
            port['ifname'],
            'UP' if port_status['link'] else 'DOWN',
            port_status['speed'],
            port_status['duplex'],
        ))
    print()


if __name__ == '__main__':
    main()
