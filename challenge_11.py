#!/usr/bin/python

'''
Challenge 11:

    Create an SSL terminated load balancer (Create self-signed certificate.)
    Create a DNS record that should be pointed to the load balancer.
    Create Three servers as nodes behind the LB.
    Each server should have a CBS volume attached to it.
    (Size and type are irrelevant.)
    All three servers should have a private Cloud Network shared between them.
    Login information to all three servers returned in a readable format as the
    result of the script, including connection information.
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

    volume_name = server.name+'_volume'
    mount_uri = "/dev/xvdd"
    print '[{0}] creating CBS volume as {1}'.format(server.name, volume_name)
    vol = cbs.create(name=volume_name, size=100)

    print '[{0}] attaching {1} as {2}'.format(server.name, volume_name, mount_uri)
    vol.attach_to_instance(server, mountpoint=mount_uri)
    pyrax.utils.wait_until(
        vol,
        "status",
        "in-use",
        interval=3,
        attempts=0,
        verbose=True
        )


# ERROR if not enough arguments supplied
if len(sys.argv) < 2:
    print '''
    Usage: {0} [FQDN]

    This script will create 2 servers and add them to a new load balancer.
    It will then create a DNS record based on [FQDN] to the load balancer.
    Finally, it will create a default error page and assign it to the load balancer.

    '''.format(sys.argv[0])
    exit()


lb_ssl_key = '''
-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDE7MGGSiht5E1H
HeOqZnqSt9JzjnGRJqPH0Aok1dcmq/SQyO+qdnzMdODbNg43iFhgjMvcPkAF5Ms/
0uMOP92KTNbMbIV266SN1XUhtgkJIErZ43hOsjVy16xG/q+4B0CS3Dxqj6CODwq7
Z80MuWJi2gP9JHDwfyVlXTw2dnxoZQ+BJne+lxM+UJppeg8kn/z+irhLGhBiIYl4
/aYj8B7Ud2usD3OurY8sPd0hoqAP7AW8nrkR0zhH46zXQOcm8Cgr9FjYDPR2sDN2
OzkQdhKRtOI49nkPnWU9QpLdXoetw98sx4dF17UQhm5LvoMck66Xvvj6683wOt7a
hsrVxAofAgMBAAECggEAXy+Jg53I2QVnjR6Xc0BBszWDVjPeFSk2NVkL7i4m5xxr
BKj7n8vSGwnLvmnsiU8wWMr1pym3zKGA1QLcmYCpVzY5BWrXQFo6mgw5p+fTikO/
qn5XIsLlLvOs5EwrJ6rpvZMS6PcvxjrjFx7fcG0Tb3CuSOgaZ0UuEEb22eR/0f1e
aA5HL1dCv43Tmx9+KbUUU/BBMiSn9mehqFb1XCUIJd7KUxKvsTL7MswJWz8Ws4O8
GkogHSDc3xAPipxGlITf+4li6ckANNahhdm8r1G7G/05c7cFOEuJn7DuyReRmeey
D5sCGfbTUytUe1Hc+3IpbKuAIBEHNswk/ay+aXunIQKBgQDgjlsXviK1T4J7o11b
itUSDLFiLj+zIu/vawQc8TcdjuZO4csZ7kPVItKXAkrv5WyvW7m4BhiDLG4Xnou6
FR8CIiQb24lEFvUZtvtlUuWEup+xLLgWahLSXQhEfYdenboWOnd0ifGCV7xqy0aP
l9/yleGOr8dZ+fv38rvGjWbwRwKBgQDgf+emS9E8mVD6zejn9T85Sv9TWH6LH76a
pyB9hRFxzg1/oC/+4t3FbukRBI60yJzrCs99BO7hZLuxCDBfzDV7cDmZTEL1KdZ+
SnryGf7UCWkYqr8xqck0YRJhbg+L1jbIMUo5hDYgzCmu4pr1AssyDW4MV/dZT6V8
6Y6RWSwbaQKBgGyxOzJw3Af65mPGHWgz+RJ1hl7JmBezb4PpvuHreAwcoSnJbS+t
/rNp2ZkyiOc5m7P9qBWFDdRgayGPon59vrafo+7AAt8sZZL+2QygZWwrkSSHSsu+
qEGeumO8hwurOOmNf0ivhHDc2tyubAcRMlsPZVBVkR7iO642leFzjEH9AoGASXiS
j1HwwCxM3EfXGVKhxlZNCTHE+DMDZgmcEHgkJWKR+FqsWnZUrfCGRhN/wJqHAEUh
coDSzODyrBVJ/5ANUMCBmTHkF+gBUoN9iQ4I38vUoUYAHHi8aG/8W/ZxEAqjExFO
gVRLgqBOY/W1UMoBRfgvM8r2IDx4pFCrX9YXIUECgYBL+S7jg/ioLv6Mb5k7RBCC
TCTLKVSr4LXuZv4TWsImZUJHWDbgFYcDvcw8+xJ0zUd3QJvB2sh22Q7G0AD5sGiY
99WtZLS6rBP9XxUZawSOUKK6+Pg5V0oH1BOiCUmu5Oyq99xZdhEQq9mffgqYYPsK
HHJ6UL8rd0F6NpGM4/MU/g==
-----END PRIVATE KEY-----
'''
lb_ssl_crt = '''
-----BEGIN CERTIFICATE-----
MIIDXTCCAkWgAwIBAgIJALkfwza4aA/dMA0GCSqGSIb3DQEBCwUAMEUxCzAJBgNV
BAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEwHwYDVQQKDBhJbnRlcm5ldCBX
aWRnaXRzIFB0eSBMdGQwHhcNMTQwNjI4MjMyMzIzWhcNMTUwNjIzMjMyMzIzWjBF
MQswCQYDVQQGEwJBVTETMBEGA1UECAwKU29tZS1TdGF0ZTEhMB8GA1UECgwYSW50
ZXJuZXQgV2lkZ2l0cyBQdHkgTHRkMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIB
CgKCAQEAxOzBhkoobeRNRx3jqmZ6krfSc45xkSajx9AKJNXXJqv0kMjvqnZ8zHTg
2zYON4hYYIzL3D5ABeTLP9LjDj/dikzWzGyFduukjdV1IbYJCSBK2eN4TrI1ctes
Rv6vuAdAktw8ao+gjg8Ku2fNDLliYtoD/SRw8H8lZV08NnZ8aGUPgSZ3vpcTPlCa
aXoPJJ/8/oq4SxoQYiGJeP2mI/Ae1HdrrA9zrq2PLD3dIaKgD+wFvJ65EdM4R+Os
10DnJvAoK/RY2Az0drAzdjs5EHYSkbTiOPZ5D51lPUKS3V6HrcPfLMeHRde1EIZu
S76DHJOul774+uvN8Dre2obK1cQKHwIDAQABo1AwTjAdBgNVHQ4EFgQUzjQzlDm2
rBlatYn8A6w1QEjtgu8wHwYDVR0jBBgwFoAUzjQzlDm2rBlatYn8A6w1QEjtgu8w
DAYDVR0TBAUwAwEB/zANBgkqhkiG9w0BAQsFAAOCAQEAHjqmXod4M0aPfVUdJ3fP
ivXfcsOxjL+MqKVAgPFTQw0FyQv3kA4cOzB3Iew1yIaGMYf283WxXIQ/+gM4t4DB
GMb+tKyu7S6y6EOWJxMcPx2sLEcFd0dPKWk6OvIZ/c+wgn71wnFEYxYTNS+wiXb2
xUtyLG+6WEgaimPDYEInlEk3wWgHfeDjBapmOhrB4dhLEw6qSRBrrFLxLw5FC+kg
6FV9tbxNF3qbmt5g5FaXDrPMyE1LMvcKXAPGIXoVaiGVZ6Hrp/S0YBiFY1h4v4TV
jV0NRklwDJbdDKo6PnQhkstwwhwk+MmHTMa+HuRB9BHD1dFTNxyFrMokbMeFUzny
hA==
-----END CERTIFICATE-----
'''
# SETUP our creds, note this expects your keyring to be setup
pyrax.keyring_auth()
cbs = pyrax.cloud_blockstorage
clb = pyrax.cloud_loadbalancers
cnw = pyrax.cloud_networks
cs = pyrax.cloudservers
dns = pyrax.cloud_dns

# WORK to do
target_cidr = '192.168.99.0/24'
target_flavor = '2'
target_fqdn = sys.argv[1]
target_image = 'bb02b1a3-bc77-4d17-ab5b-421d89850fca'
target_lb = 'dearing-lb11'
target_prefix = 'dearing_'
target_suffix = '_lb11'
target_network = 'dearing-chal11'
targets = ['web1', 'web2', 'web3']

# create our private network
print 'creating private network {0}'.format(target_cidr)
network = cnw.create(target_network, cidr=target_cidr)

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
        nics=network.get_server_networks(public=True, private=True),
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

# IMPLEMENT SSL TERMINATION
pyrax.utils.wait_until(lb, "status", "ACTIVE")
print 'adding ssl termination to {0}'.format(target_lb)
lb.add_ssl_termination(
    securePort=443,
    enabled=True,
    secureTrafficOnly=False,
    certificate=lb_ssl_crt,
    privatekey=lb_ssl_key
    )

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
