#!/usr/bin/python

'''
Challenge 4: Write a script that uses Cloud DNS to create a new A record 
when passed a FQDN and IP address as arguments.
INCOMPLETE
'''

import sys
import pyrax


# SETUP our creds, note this expects your keyring to be setup
pyrax.keyring_auth()
dns = pyrax.cloud_dns

# DNS default adjustment
dns.set_timeout(30)
dns.set_delay(1)

# ERROR if not enough arguments supplied
if len(sys.argv) < 3:
    print '''
    Usage: {0} [FQDN] [IP]

    This script will create a new A record based on the supplied
    FQDN and IP.

    '''.format(sys.argv[0])
    exit()

fqdn = sys.argv[1]
ip = sys.argv[2]

# Getting authentication errors, cannot test
record = {"type": "A", "data": ip}
dom = dns.create(
    name=fqdn,
    emailAddress="jacob.dearing@gmail.com",
    records=[record])
