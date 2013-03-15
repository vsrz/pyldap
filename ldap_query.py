#!/usr/bin/python
#
# Ldap query on an DN and write to file
#
#
#

import sys
import time
import ldap

f = open('out.txt','w')

LDAP_PROTO = ''
LDAP_SERVER = ''
LDAP_BIND_DN = ''
LDAP_BIND_PW = ''

# Setup Search params
LDAP_BASEDN = 'ou=People,dc=example,dc=com'
LDAP_SEARCH_SCOPE = ldap.SCOPE_SUBTREE

# Retrieve attributes
RETRIEVE_ATTRIBUTES = ['uid','pwdAccountLockedTime']
SEARCH_FILTER = 'pwdAccountLockedTime=*'


# Setup LDAP Conn
try:

        l = ldap.initialize(LDAP_PROTO + '://' + LDAP_SERVER)

        l.protocol_version = ldap.VERSION3

        username = LDAP_BIND_DN
        password = LDAP_BIND_PW

        l.simple_bind_s(username,password)

except ldap.LDAPError, e:
        print e


try:
        ldap_result = l.search_s(LDAP_BASEDN, ldap.SCOPE_SUBTREE, SEARCH_FILTER, RETRIEVE_ATTRIBUTES)
        for dn,entry in ldap_result:
                acct = str(dn)
                f.write(acct + '\n')

except ldap.LDAPError, e:
        print 'Error %s retrieving' % str(e)


