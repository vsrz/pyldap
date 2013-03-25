#!/usr/bin/python
#
# Runs ldap query with paginated results for result sets > 1000 in AD
#
#

from ldap.ldapobject import LDAPObject
import ldap,pprint
from ldap.controls import SimplePagedResultsControl
import sys
import time

# Setup LDAP Conn
try:

	ad = ldap.initialize('ldap://')

	ad.protocol_version = ldap.VERSION3

	username = ''
	password = ''

	ad.simple_bind_s(username,password)

except ldap.LDAPError, e:
	print e

# Setup Search params
baseDN = 'ou=People,dc=example,dc=com'
searchScope = ldap.SCOPE_SUBTREE
pageSize = 1000

# Retrieve only whats needed
retrieveAttributes = ['sAMAccountName','displayName','description','employeeID','whenCreated','mail']
searchFilter = 'sAMAccountName=*'

# Setup paged result control
page = 0
serverctrls = None

try: 
	req_ctrl = SimplePagedResultsControl( ldap.LDAP_CONTROL_PAGE_OID, True, (pageSize, ''))
	ldap_result_id = ad.search_ext(baseDN, searchScope, searchFilter, retrieveAttributes, serverctrls=(serverctrls or []) + [req_ctrl])
	result_pages = 0
	result_set = []
	while 1:
		rtype, rdata, rmsgid, rctrls = ad.result3(ldap_result_id)
		result_set.extend(rdata)
		result_pages += 1
		
		#extract the simple paged results response control
		pctrls = [
			c
			for c in rctrls
			if c.controlType == SimplePagedResultsControl.controlType
		]
		if pctrls:
			est, cookie = pctrls[0].controlValue
			if cookie:
				# copy the cookie from the response control to the request control
				req_ctrl.controlValue = (pageSize, cookie)
				ldap_result_id = ad.search_ext(baseDN, searchScope, searchFilter, retrieveAttributes, serverctrls=(serverctrls or []) + [req_ctrl])
			else:
				break
	
	x = 0
	# print results with column headers
	print "sAMAccountName, displayName, description, employeeID, whenCreated, mail"
	for e in result_set:
		x += 1
		info = e[1]
		msg = ''
		if 'sAMAccountName' in info:
			msg += info['sAMAccountName'][0]
		msg += ','

		if 'displayName' in info:
			msg += info['displayName'][0]
		msg += ','

		if 'description' in info:
			msg += info['description'][0]
		msg += ','

		if 'employeeID' in info:
			msg += info['employeeID'][0]
		msg += ','

		if 'whenCreated' in info:
			msg += info['whenCreated'][0][0:8]
		msg += ','

		if 'mail' in info:
			msg += info['mail'][0]

		print msg	

except ldap.LDAPError, e:
	print e
	exit

