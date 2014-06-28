#!/usr/bin/python

'''
Challenge 2: Write a script that clones a server 
(takes an image and deploys the image as a new server)
'''

import pyrax

# SETUP our creds, note this expects your keyring to be setup
pyrax.keyring_auth()
cs = pyrax.cloudservers

# SETUP our server deets
image_name = 'dearing-base_image'
server_name = 'dearing-base_test'
server_flavor = '2'

print 'fetching servers list to clone from...'
for server in cs.servers.list():
    print '{0} : {1}'.format(server.id, server.name)

# EXPECT server id
selection = raw_input('enter server ID to clone: ')

print 'creating image of {0} as `{1}`'.format(selection, image_name)
image_id = cs.servers.create_image(selection, image_name)
image = cs.images.get(image_id)

print 'waiting for image {0} `{1}` to finish...'.format(image.id, image.name)
image = pyrax.utils.wait_until(image, 'status', ['ACTIVE', 'ERROR'])

print 'creating server `{0}` based on {1} as flavor {2}'.format(
    server_name,
    image.id,
    server_flavor
    )

server = cs.servers.create(name=server_name, image=image.id, flavor=server_flavor)
pyrax.utils.wait_for_build(server)

print '{0} created; now deleting...'.format(server.name)
server.delete()
