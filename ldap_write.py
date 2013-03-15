#!/usr/bin/python
#
# Writes lock data to a list of DN's found in file
#

import sys
import time
import ldap
import datetime
from Rsa import RsaSecurity

f = open('input.txt','r')
log = open('lock.log','a')

LDAP_PROTO = 'ldaps'
LDAP_SERVER = ''
LDAP_BIND_DN = ''
LDAP_BIND_PW = ''

# Setup Search params
LDAP_BASEDN = 'ou=People,dc=example,dc=com'
LDAP_SEARCH_SCOPE = ldap.SCOPE_SUBTREE
SEARCH_FILTER = '(%s)'
RETRIEVE_ATTRIBUTES = ['dn','pwdAccountLockedTime']

# Set the lock time we will use to re-lock accounts
dt = datetime.datetime.now()
timestamp = str(dt.year).zfill(4) + str(dt.month).zfill(2) + str(dt.day).zfill(2) + str(dt.hour).zfill(2) + str(dt.minute).zfill(2) + str(dt.second).zfill(2) + str('-0800')

# Setup LDAP Conn
try:

        l = ldap.initialize(LDAP_PROTO + '://' + LDAP_SERVER)

        l.protocol_version = ldap.VERSION3

        username = LDAP_BIND_DN
        password = LDAP_BIND_PW

        l.simple_bind_s(username,password)

except ldap.LDAPError, e:
        print e

for each_account in f:
        try:
                # perform search first to see if we need to relock this
                dn = each_account.split(',')
                ldap_result = l.search_s(LDAP_BASEDN, ldap.SCOPE_SUBTREE, SEARCH_FILTER % dn[0], RETRIEVE_ATTRIBUTES)

                if ldap_result:
                        for dn,entry in ldap_result:
                                # if pwdAccountLockedTime is not set, set it
                                if not entry:
                                        mod_attrs = [(ldap.MOD_ADD, 'pwdAccountLockedTime',timestamp)]
                                        l.modify_s(each_account, mod_attrs)

                else:
                        # if a locked account was deleted, trigger this
                        log.write(str(datetime.datetime.now()) + ' dn %s does not exist\n' % each_account.replace('\n',''))

        except ldap.LDAPError, e:
                log.write(str(datetime.datetime.now()) + ' dn %s %s\n' % (each_account.replace('\n',''),str(e)))


