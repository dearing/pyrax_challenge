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

cf = pyrax.cloudfiles
cs = pyrax.cloudservers
cbs = pyrax.cloud_blockstorage
cdb = pyrax.cloud_databases
clb = pyrax.cloud_loadbalancers
cnw = pyrax.cloud_networks
dns = pyrax.cloud_dns

target = 'dearing'
suffix = 'dearing.link'

print 'Hunting targets starting with', target

# NUKE SERVERS starting with target
print 'Searching cloud servers'
for server in cs.servers.list():
    if server.name.startswith(target):
        print '-- nuke {0} {1}'.format(server.id, server.name)
        server.delete()

print 'Searching cloud server images'
for image in cs.list_images():
    if image.human_id.startswith(target):
        print '-- nuke {0} {1} {2}'.format(image.id, image.name, image.status)
        image.delete()

print 'Searching cloud block storage'
for block in cbs.list():
    if block.name.startswith(target):
        print '-- nuke {0} {1}'.format(block.id, block.name)
        block = pyrax.utils.wait_until(block, 'status', 'available')
        block.delete()

print 'Searching cloud databases'
for instance in cdb.list():
    if instance.name.startswith(target):
        print '-- nuke {0} {1}'.format(instance.id, instance.name)
        instance.delete()

print 'Searching cloud load balancers'
for lb in clb.list():
    if lb.name.startswith(target):
        print '-- nuke {0} {1}'.format(lb.id, lb.name)
        lb = pyrax.utils.wait_until(lb, 'status', ['ACTIVE', 'ERROR'])
        lb.delete()

print 'Searching containers'
for con in cf.list():
    if con.name.startswith(target):
        print '-- nuke {0} {1}'.format(con.id, con.name)

print 'Searching cloud networks'
for nw in cnw.list():
    if nw.label.startswith(target):
        print '-- nuke {0} {1} {2}'.format(nw.id, nw.label, nw.cidr)
        nw.delete()

print 'Searching cloud dns'
for dom in dns.list():
    if dom.name.endswith(suffix):
        print '-- nuke {0} {1} '.format(dom.id, dom.name)
        dom.delete(delete_subdomains=True)

print 'Done.'
