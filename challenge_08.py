#!/usr/bin/python

'''
Challenge 8: Write a script that will create a static webpage served out of
Cloud Files. The script must create a new container, cdn enable it, enable it
to serve an index file, create an index file object, upload the object to the
container, and create a CNAME record pointing to the CDN URL of the container.
'''

import pyrax


# SETUP our creds, note this expects your keyring to be setup
pyrax.keyring_auth()
cf = pyrax.cloudfiles
dns = pyrax.cloud_dns

index = '''
<html>
<head>
<title>challenge_08</title>
</head>
<body>hello challenge_08!</body>
</html>
'''

container_name = 'dearing-chal08'
cname_target = 'chal08.dearing.systems'

print 'creating container {0}'.format(container_name)
con = cf.create_container(container_name)

print 'making {0} public'.format(container_name)
con.make_public()

con = cf.get_container(container_name)
print '{0}.cdn_uri => {1}'.format(container_name, con.cdn_uri)

chksum = pyrax.utils.get_checksum(index)
print 'storing index.html to {0} // chksum {1}'.format(container_name, chksum)
con.store_object('index.html', index, etag=chksum)

print 'setting {0} to host index.html'.format(container_name)
con.set_web_index_page('index.html')

# UNABLE to complete DNS targets at this time
print 'CNAME would be {0} {1}'.format(con.cdn_uri, cname_target)
