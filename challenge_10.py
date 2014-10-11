#!/usr/bin/python

'''
Challenge 10: Write an application that will:

    Create 2 servers, supplying a ssh key to be installed at /root/.ssh/authorized_keys.
    Create a load balancer
    Add the 2 new servers to the LB
    Set up LB monitor and custom error page.
    Create a DNS record based on a FQDN for the LB VIP.
    Write the error page html to a file in cloud files for backup.

'''

import sys
import pyrax


def server_callback(server):
    '''
    ON CALLBACK -
        report server
        create node for server
        add server to load balancer
    '''
    print '[{0}] created as {1}; use keypair {2} with public ip {3}'.format(
        server.name,
        server.id,
        server.key_name,
        server.networks['public'][1]
        )

    ip = server.networks['private'][0]
    node = clb.Node(
        address=ip,
        port="80",
        condition="ENABLED"
        )

    print '[{0}] creating node for {1}; awaiting'.format(target_lb, node.address)
    pyrax.utils.wait_until(lb, "status", "ACTIVE")

    lb.add_nodes([node])
    pyrax.utils.wait_until(lb, "status", "ACTIVE")
    print '[{0}] node {1} added for {2}'.format(target_lb, node.address, server.name)

# ERROR if not enough arguments supplied
if len(sys.argv) < 2:
    print '''
    Usage: {0} [FQDN]

    This script will create 2 servers and add them to a new load balancer.
    It will then create a DNS record based on [FQDN] to the load balancer.
    Finally, it will create a default error page and assign it to the load balancer.

    '''.format(sys.argv[0])
    exit()
# SETUP our creds, note this expects your keyring to be setup
pyrax.keyring_auth()
clb = pyrax.cloud_loadbalancers
cs = pyrax.cloudservers
dns = pyrax.cloud_dns

# WORK to do
target_flavor = '2'
target_fqdn = sys.argv[1]
target_image = 'bb02b1a3-bc77-4d17-ab5b-421d89850fca'
target_lb = 'dearing-lb10'
target_prefix = 'dearing_'
target_suffix = '_lb10'
targets = ['web1', 'web2']

# Create our load balancer; async operation converge at server callback
vip = clb.VirtualIP(type="PUBLIC")
lb = clb.create(target_lb, port=80, protocol="HTTP", virtual_ips=[vip])
print 'created {0} with with {1} vip'.format(target_lb, vip.type)

# iterate through our WORK,
# create the server and assign the callback to report and delete
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

# DESIGN our customer error_page
error_page = '''
<html>
<head>
<title>challenge_10</title>
</head>
<body>error page for challenge 10</body>
</html>
'''

# ASSIGN our error_page to this LB when ready
pyrax.utils.wait_until(lb, "status", "ACTIVE")
lb.set_error_page(error_page)
print 'custom error page added to {0}'.format(target_lb)

# DESIGN our records for FQDN
lb_ip = lb.virtual_ips[0].address
recs = [{
        "type": "A",
        "data": lb_ip,
        "ttl": 300,
        "name": target_fqdn
        }]

# ATTEMPT to create target_fqdn with records
try:
    dom = dns.create(
        name=target_fqdn,
        emailAddress='admin@'+target_fqdn,
        comment='challenge_10',
        records=recs
        )
    pass
except pyrax.exceptions.DomainCreationFailed:
    print 'unable to create {0}'.format(target_fqdn)
    exit()
except Exception, e:
    raise

print 'created A record for {0} to {1}'.format(target_fqdn, lb_ip)

# WAIT for server threads to complete
print 'awaiting threads to converge'
