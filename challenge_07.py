#!/usr/bin/python

'''
Challenge 7: Write a script that will create 2 Cloud Servers and
add them as nodes to a new Cloud Load Balancer.
'''

import pyrax


def server_callback(server):
    '''
    ON CALLBACK - add this server to our LB awaiting status
    '''
    ip = server.networks['private'][0]
    node = clb.Node(
        address=ip,
        port="80",
        condition="ENABLED"
        )

    print '[{0}] creating node for {1}; awaiting'.format(lb_name, node.address)
    pyrax.utils.wait_until(lb, "status", "ACTIVE")
    lb.add_nodes([node])
    pyrax.utils.wait_until(lb, "status", "ACTIVE")
    print '[{0}] node {1} added'.format(lb_name, node.address)


# SETUP our creds, note this expects your keyring to be setup
pyrax.keyring_auth()
cs = pyrax.cloudservers
clb = pyrax.cloud_loadbalancers

# WORK to do
lb_name = 'dearing-lb0'
targets = ['web1', 'web2']
target_prefix = 'dearing_'
target_suffix = '_lb0'
target_flavor = '2'
target_image = 'bb02b1a3-bc77-4d17-ab5b-421d89850fca'

# Create our load balancer; async operation converge at callback
vip = clb.VirtualIP(type="PUBLIC")
lb = clb.create(lb_name, port=80, protocol="HTTP", virtual_ips=[vip])
print 'created {0} with {1} vip'.format(lb_name, vip.type)

# create the servers and assign the callback to add the nodes to the lb
for target in targets:
    target_name = target_prefix + target + target_suffix
    print '[{0}] creating as flavor {1} with image {2}'.format(
        target_name,
        target_flavor,
        target_image
        )
    server = cs.servers.create(
        target_name,
        target_image,
        target_flavor,
        key_name='dearing'  # must exist in this region to succeed
        )
    pyrax.utils.wait_for_build(server, callback=server_callback)

print 'awaiting threads to converge'
