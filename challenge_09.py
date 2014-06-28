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

print 'creating AAAA record for {0} to {1}'.format(
    fqdn,
    server.networks['public'][0]
    )

print 'creating A record for {0} to {1}'.format(
    fqdn,
    server.networks['public'][1]
    )

print 'deleting {0} {1}'.format(server.name, server.id)
server.delete()
