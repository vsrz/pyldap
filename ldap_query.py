import ldap
import sys
import time

# Setup LDAP Conn
try:

	l = ldap.open('')

	l.protocol_version = ldap.VERSION3

	username = ''
	password = ''

	l.simple_bind(username,password)

except ldap.LDAPerror, e:
	print e

# Setup Search params
baseDN = 'ou=students,ou=academic,dc=csusm,dc=edu'
searchScope = ldap.SCOPE_SUBTREE

# Retrieve only whats needed
#retrieveAttributes = ['sAMAccountName','employeeID','mail']
retrieveAttributes = ['sAMAccountName','displayName','description','employeeID','whenCreated','mail']
#searchFilter = 'sAMAccountName=ville017'
searchFilter = 'whenCreated=20120622223453.0Z';

try: 
	ldap_result_id = l.search(baseDN, searchScope, searchFilter, retrieveAttributes)
	result_set = []
	while 1:
		result_type, result_data = l.result(ldap_result_id, 0)
		if(result_data == []):
			break
		else:
			if result_type == ldap.RES_SEARCH_ENTRY:
				result_set.append(result_data)
	#print result_set

	# result set
	x = 0
	for each in result_set:
		# re
		for e in each:
			x += 1
			print str(e[1]['sAMAccountName'][0]) + ',' + str(e[1]['displayName'][0]) + ',' +str(e[1]['description'][0]) + ',' +str(e[1]['employeeID'][0]) + ',' + str(e[1]['whenCreated'][0][0:8]) + ',' + str(e[1]['mail'][0])
except ldap.LDAPError, e:
	#print e
	exit
