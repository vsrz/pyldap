import ldap
import sys
import time

f = open('ad-samids.txt','r')


# Setup LDAP Conn
try:

	l = ldap.open('')

	l.protocol_version = ldap.VERSION3

	username = ''
	password = ''

	l.simple_bind(username,password)

except ldap.LDAPerror, e:
	print e
for each in f:
	# Setup Search params
	baseDN = 'dc=csusm,dc=edu'
	searchScope = ldap.SCOPE_SUBTREE

	# Retrieve only whats needed
	#retrieveAttributes = ['sAMAccountName','employeeID','mail']
	retrieveAttributes = ['sAMAccountName','displayName','description','employeeID','whenCreated','mail']
	searchFilter = 'uid=%s' % (unicode(str(each.rstrip('\n'))))
	#searchFilter = 'sAMAccountName=' + str(each)
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

		# result set
		x = 0
		if len(result_set) < 1:
			print '%s' % (str(each.rstrip('\n')))
	except ldap.LDAPError, e:
		print 'Error %s retrieving: %s' % (str(e),each)

