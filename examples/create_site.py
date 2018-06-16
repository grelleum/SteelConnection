import steelconnection

# Change the below values to match the realm and org as seen in the URL for your SteelConnect Manager.
# for example:  https://realm.riverbed.cc/admin/TestLab
scm_name = 'realm.riverbed.cc'
org_name = 'TestLab'   

# Details for the site to be created:
new_site = {
    'name': 'NYC',
    'city': 'New York',
    'country': 'US',
    'longname': 'New York test lab.',
    'timezone': 'America/New_York',
}

# Initialize the steelconnection object.
sconnect = steelconnection.SConAPI(scm_name)

# Get the org ID for your organization.
org_id, org = sconnect.lookup.org(org_name)
print('Org name: {},  org_id: {}'.format(org_name, org_id))

# API resource for posting.
resource = '/org/{}/sites'.format(org_id)

# Make the post request.
result = sconnect.post(resource, data=new_site)

# Display response.
print('Response:', sconnect.response.status_code, sconnect.response.reason)
print(result)