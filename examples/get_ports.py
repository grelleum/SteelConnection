"""List port information for a SteelConnect appliance."""

from __future__ import print_function

import steelconnection

print("Note: SteelConnect Realm is usually in the form 'realm.riverbed.cc'")
realm = steelconnection.get_input('Please enter your SteelConnect Realm: ')
sc = steelconnection.SConAPI(realm)

appliance = steelconnection.get_input('\nPlease enter the appliance serial number: ')
node_id, node = sc.lookup.node(appliance)

ports = sc.get('node/' + node_id + '/ports')

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
