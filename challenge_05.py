#!/usr/bin/python

'''
Challenge 5: Write a script that creates a Cloud Database instance.
This instance should contain at least one database, and the database
should have at least one user that can connect to it.
'''

import pyrax

# SETUP our creds, note this expects your keyring to be setup
pyrax.keyring_auth()
cdb = pyrax.cloud_databases

# SETUP some nice values
instance_name = 'dearing-challenge05'
database_name = 'chumpypress'
database_user = 'chumpy'
database_pass = 'Chumpy!14'

print 'availiable flavors:'
for db in cdb.list_flavors():
    print db.name, db.ram

# CREATE INSTANCE
print 'creating {0}'.format(instance_name)
instance = cdb.create(instance_name, flavor=1, volume=1)
print '{0}'.format(instance)
pyrax.utils.wait_for_build(instance)

# CREATE DATABASE in INSTANCE
print 'creating {0}'.format(database_name)
database = instance.create_database(database_name)
print '{0}'.format(database)

# CREATE USER in DATABASE in INSTANCE
print 'creating user {0} with {1}'.format(database_user, database_pass)
user = instance.create_user(
    name=database_name,
    password=database_pass,
    database_names=[database],
    host="%")
print '{0}'.format(user)

# DESTROY this INSTANCE
print 'deleting {0}'.format(instance_name)
instance.delete()
