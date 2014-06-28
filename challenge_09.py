#!/usr/bin/python

'''
Challenge 9: Write an application that when passed the arguments FQDN, image,
and flavor it creates a server of the specified image and flavor with the same
name as the fqdn, and creates a DNS entry for the fqdn pointing to the server's
public IP.
'''

import sys
import pyrax


# SETUP our creds, note this expects your keyring to be setup
pyrax.keyring_auth()
cs = pyrax.cloudservers
dns = pyrax.cloud_dns

# ERROR if not enough arguments supplied
if len(sys.argv) < 4:
    print '''
    Usage: {0} [FQDN] [flavor] [image]

    This script will create a server named [FQDN] as flavor [flavor]
    from image [image] and then update DNS for [FQDN] to point to the
    server's public IP.

    '''.format(sys.argv[0])
    exit()

fqdn = sys.argv[1]
flavor = sys.argv[2]
image = sys.argv[3]

print 'creating {0} as flavor {1} with image {2}'.format(fqdn, flavor, image)
server = cs.servers.create(fqdn, image, flavor)

print 'waiting for build to complete....'
pyrax.utils.wait_for_build(server)

# DESIGN our records for FQDN
recs = [{
        "type": "AAAA",
        "data": server.networks['public'][0],
        "ttl": 300,
        "name": fqdn
        }, {
        "type": "A",
        "data": server.networks['public'][1],
        "ttl": 300,
        "name": fqdn
        }]

# ATTEMPT to create FQDN with records
try:
    dom = dns.create(
        name=fqdn,
        emailAddress='admin@'+fqdn,
        comment='challenge_09',
        records=recs
        )
    pass
except pyrax.exceptions.DomainCreationFailed:
    print 'unable to create {0}'.format(fqdn)
    exit()
except Exception, e:
    raise

print 'created AAAA record for {0} to {1}'.format(
    fqdn,
    server.networks['public'][0]
    )

print 'created A record for {0} to {1}'.format(
    fqdn,
    server.networks['public'][1]
    )
