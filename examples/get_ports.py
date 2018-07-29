"""List port information for a SteelConnect appliance."""

from __future__ import print_function

import steelconnection


appliance = steelconnection.get_input(
    'Enter the appliance serial number: '
)

print("Note: SteelConnect Realm is usually in the form 'realm.riverbed.cc'")
sc = steelconnection.SConAPI()
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
