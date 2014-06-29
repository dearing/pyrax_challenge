#!/usr/bin/python

'''
Challenge 13:
This one might need to be altered to a particular region etc.. 
Don't wipe out servers you want to keep on your account obviously!! 
Write an application that nukes everything in your Cloud Account. It should:
    Delete all Cloud Servers
    Delete all Custom Images
    Delete all Cloud Files Containers and Objects
    Delete all Databases
    Delete all Networks
    Delete all CBS Volumes

'''

import pyrax

# SETUP our creds, note this expects your keyring to be setup
pyrax.keyring_auth()

cbs = pyrax.cloud_blockstorage
cdb = pyrax.cloud_databases
cf = pyrax.cloudfiles
clb = pyrax.cloud_loadbalancers
cnw = pyrax.cloud_networks
cs = pyrax.cloudservers
dns = pyrax.cloud_dns

target = 'dearing'

# NUKE SERVERS starting with target
for server in cs.servers.list():
    if server.name.startswith(target):
        print '[CSs] would nuke {0} - {1}'.format(server.id, server.name)

for image in cs.images.list():
    if image.name.startswith(target):
        print '[CSi] would nuke {0} - {1}'.format(server.id, server.name)

for block in cbs.list():
    if block.name.startswith(target):
        print '[CBS] would nuke {0} {1}'.format(block.id, block.name)

for instance in cdb.list():
    if instance.name.startswith(target):
        print '[CDB] would nuke {0} {1}'.format(instance.id, instance.name)

for lb in clb.list():
    if lb.name.startswith(target):
        print '[CLB] would nuke {0} {1}'.format(lb.id, lb.name)

for con in cf.list():
    if con.name.startswith(target):
        print '[ CF] would nuke {0} {1}'.format(con.id, con.name)

try:
    for network in cnw.find_network_by_label(target):
        print '[CNW] would nuke {0} {1}'.format(network.id, network.name)
except:
    pass

try:
    for network in cnw.find_network_by_name(target):
        print '[CNW] would nuke {0} {1}'.format(network.id, network.name)
except:
    pass

print 'Done.'
