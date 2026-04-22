# encoding: utf-8

'''🧠 LabCAS Infosphere: constants.'''


DEFAULT_SOLR_URL = 'https://localhost:8984/solr/'
DEFAULT_PORT = 8998

DEFAULT_LDAP_URI = 'ldaps://edrn-ds.jpl.nasa.gov'
DEFAULT_GROUP_DN = 'cn=Portal Content Custodian,dc=edrn,dc=jpl,dc=nasa,dc=gov'
USER_DN_TEMPLATE = 'uid={username},dc=edrn,dc=jpl,dc=nasa,dc=gov'

SOLR_ROWS = 1000
SOLR_SORT = 'id asc'
