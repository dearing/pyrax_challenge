#!/usr/bin/python

'''
Challenge 1: Write a script that builds three 512 MB Cloud Servers that
following a similar naming convention. (ie., web1, web2, web3) and returns the
IP and login credentials for each server. Use any image you want.
'''

import pyrax


def server_callback(server):
    '''
    ON CALLBACK - report some stats and destroy our work
    server is the 'refreshed' SERVER, following ACTIVE or ERROR status
    '''
    print '[{0}] created as {1}; use keypair {2} with public ip {3}'.format(
        server.name,
        server.id,
        server.key_name,
        server.networks['public'][1]
        )
    server.delete()
    print '[{0}] `{1}` deleted.'.format(server.name, server.id)

# SETUP our creds, note this expects your keyring to be setup
pyrax.keyring_auth()
cs = pyrax.cloudservers

# WORK to do
targets = ['web1', 'web2', 'web3']
target_prefix = 'dearing_'
target_suffix = ''
target_flavor = '2'
target_image = 'bb02b1a3-bc77-4d17-ab5b-421d89850fca'

# iterate through our WORK,
# create the server and assign the callback to report and delete
for target in targets:
    target_name = target_prefix + target + target_suffix
    print '[{0}] creating as flavor {1} with image {2}'.format(
        target_name,
        target_flavor,
        target_image
        )
    exit
    server = cs.servers.create(
        target_name,
        target_image,
        target_flavor,
        key_name='dearing'  # must exist in this region to succeed
        )
    pyrax.utils.wait_for_build(server, callback=server_callback)

print 'awaiting threads to converge'