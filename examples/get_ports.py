"""List port information for a SteelConnect appliance."""

import steelconnection

print("SteelConnect Realm should be entered in the for 'realm.riverbed.cc'")
realm = steelconnection.get_input('Please enter your SteelConnect Realm: ')
sconnect = steelconnection.SConAPI(realm)

appliance = steelconnection.get_input('Please enter the appliance serial number: ')
node_id, node = sconnect.lookup.node(appliance)

ports = sconnect.get('node/' + node_id + '/ports')

line = '{:14}{:10}{:8}{:8}{:8}'
print(line.format('Port ID', 'ifname', 'Link', 'Speed', 'Duplex'))
print(line.format('-------', '------', '----', '-----', '------'))

for port in ports:
    resource = 'port/{}'.format(port['id'])
    port_status = sconnect.getstatus(resource)
    print(line.format(
        port['port_id'],
        port['ifname'],
        'UP' if port_status['link'] else 'DOWN',
        port_status['speed'],
        port_status['duplex'],
    ))
