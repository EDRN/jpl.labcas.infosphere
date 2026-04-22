# encoding: utf-8

'''🧠 LabCAS Infosphere: LDAP authentication and group membership.'''

from __future__ import annotations

from ldap3 import BASE, Connection, Server
from ldap3.core.exceptions import LDAPException
from ldap3.utils.conv import escape_filter_chars


def user_dn(username: str, template: str) -> str:
    '''Return the LDAP bind DN for `username` using `template` (`{username}` placeholder).'''
    return template.replace('{username}', username)


def authenticate_and_in_group(uri: str, bind_dn: str, password: str, group_dn: str) -> bool:
    '''Bind with `bind_dn` and `password`, then verify `group_dn` lists that DN in `uniqueMember`.

    Returns True if the user is authenticated and a member of the group, False otherwise.
    '''
    server = Server(uri)
    conn = Connection(server, user=bind_dn, password=password, auto_bind=False)
    try:
        if not conn.bind():
            return False
        filt = f'(uniqueMember={escape_filter_chars(bind_dn)})'
        conn.search(group_dn, filt, search_scope=BASE, attributes=['1.1'])
        return conn.result['result'] == 0 and len(conn.entries) == 1
    except LDAPException:
        return False
    finally:
        try:
            conn.unbind()
        except LDAPException:
            pass
