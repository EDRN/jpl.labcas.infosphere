# encoding: utf-8

'''🧠 LabCAS Infosphere: constants.'''


DEFAULT_SOLR_URL = 'https://localhost:8984/solr/'
DEFAULT_PORT     = 8998

DEFAULT_LDAP_URI = 'ldaps://edrn-ds.jpl.nasa.gov'
DEFAULT_GROUP_DN = 'cn=API Users,dc=edrn,dc=jpl,dc=nasa,dc=gov'
USER_DN_TEMPLATE = 'uid={username},dc=edrn,dc=jpl,dc=nasa,dc=gov'

SOLR_ROWS = 1000
SOLR_SORT = 'id asc'

DMCC_CLIENT_ID    = '59502649ee224c2fa58362d336e4c92c'
DMCC_TOKEN_API    = 'https://www.compass.fhcrc.org/edrnauthapi/auth/token'
DMCC_IMAGE_EVENTS = 'https://www.compass.fhcrc.org/edrnrestws/Data/GetAllImageEvents'

PROTOCOL_IDS = {
    'Lung_Team_Project_2': 354,
    'Prostate_MRI': 430,
}