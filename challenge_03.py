#!/usr/bin/python

'''
Challenge 3: Write a script that accepts a directory as an argument as well as
a container name. The script should upload the contents of the specified
directory to the container (or create it if it doesn't exist). The script
should handle errors appropriately. (Check for invalid paths, etc.)
'''

import os
import sys
import pyrax


# SETUP our creds, note this expects your keyring to be setup
pyrax.keyring_auth()
cf = pyrax.cloudfiles

# ERROR if not enough arguments supplied
if len(sys.argv) < 3:
    print '''
    Usage: {0} [path] [container_name]

    This script will copy all files in a given [path] to a [container]
    on the cloud files using pyrax.

    '''.format(sys.argv[0])
    exit()

path = sys.argv[1]
container_name = sys.argv[2]

# ERROR if path !extant
if not os.path.exists(path):
    print path, 'does not exist!'
    exit()

print 'uploading {0} to container {1}'.format(path, container_name)
container = cf.create_container(container_name)
cf.sync_folder_to_container(path, container)
