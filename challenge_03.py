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
container = sys.argv[2]

# ERROR if path !extant
if not os.path.exists(path):
    print path, 'does not exist!'
    exit()

print 'uploading {0} to container {1}'.format(path, container)

# CREATE container will return extant (non-distructive)
cf.create_container(container)

# TEST for dir and upload file
for f in os.listdir(path):
    file = path+'/'+f
    if os.path.isfile(file):
        chksum = pyrax.utils.get_checksum(file)
        print 'uploading {0} to {1}'.format(file, container)
        obj = cf.upload_file(container, file, etag=chksum)
        print 'OK : {0} => {1}'.format(obj.name, obj.etag)
