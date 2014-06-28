#!/usr/bin/python

'''
Challenge 6: Write a script that creates a CDN-enabled
container in Cloud Files.
'''

import sys
import pyrax


# SETUP our creds, note this expects your keyring to be setup
pyrax.keyring_auth()
cf = pyrax.cloudfiles

# ERROR if not enough arguments supplied
if len(sys.argv) < 2:
    print '''
    Usage: {0} [container_name]

    Publish a [container_name] to CDN.

    '''.format(sys.argv[0])
    exit()

container_name = sys.argv[1]
container = cf.create_container(container_name)
container.make_public()

print '{0} made public: '.format(container_name)
container = cf.get_container(container_name)
print container.cdn_enabled, container.cdn_uri, container.cdn_ttl
