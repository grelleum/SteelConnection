"""List port information for a SteelConnect appliance."""

import steelconnection

realm = steelconnection.get_input('Please enter your SteelConnect Realm: ')
sconnect = steelconnection.SConAPI(realm)

appliance = steelconnection.get_input('Please enter the appliance serial number: ')
node_id = sconnect.lookup.nodeid(appliance)

ports = sconnect.config.get(f'node/{node_id}/ports').data

print('\nPort ID \tifname \tLink \tSpeed \tDuplex')
print('------- \t------ \t---- \t----- \t------')

for port in ports:
    resource = 'port/{}'.format(port['id'])
    port_status = sconnect.report.get(resource).data

    print('{}\t{}\t{}\t{}\t{}'.format(
        port['port_id'],
        port['ifname'],
        'UP' if port_status['link'] else 'DOWN',
        port_status['speed'],
        port_status['duplex'],
    ))
