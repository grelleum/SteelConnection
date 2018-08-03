
# coding: utf-8

# ```
#    ______          _______                       __  _
#   / __/ /____ ___ / / ___/__  ___  ___  ___ ____/ /_(_)__  ___
#  _\ \/ __/ -_) -_) / /__/ _ \/ _ \/ _ \/ -_) __/ __/ / _ \/ _ \
# /___/\__/\__/\__/_/\___/\___/_//_/_//_/\__/\__/\__/_/\___/_//_/
# ```
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
print(sc)

serial = steelconnection.get_input('Enter the serial number of the appliance: ')
node = sc.lookup.node(serial)

# find user home directory
home = os.path.expanduser('~')
filename = 'scon_vgw_{}.zip'.format(serial.upper())

# join the home dir, 'Downloads', and filename:
filepath = os.path.join(home, 'Downloads', filename)

hypervisor = steelconnection.get_input('Enter the hypervisor type: ')
success = sc.download_image(node['id'], save_as=filename, build=hypervisor)
print(success)
