
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


from __future__ import print_function

import steelconnection
import os

sc = steelconnection.SConAPI()
sc.get('status')

# steelconnection.get_input function is compatible with both Python 2 and 3.
serial = steelconnection.get_input('Enter appliance serial number: ')
node = sc.lookup.node(serial)

hypervisor = steelconnection.get_input('Enter the hypervisor type: ')
filename = 'scon_vgw_{}_{}.zip'.format(serial, hypervisor)

# Put filename into the HOME/Downloads folder.
home = os.path.expanduser('~')
filepath = os.path.join(home, 'Downloads', filename)

success = sc.download_image(node['id'], save_as=filename, build=hypervisor)
print(success)
