# encoding: utf-8

'''🧠 LabCAS Infosphere: argument parsing.'''


from . import VERSION
from .const import (
    DEFAULT_GROUP_DN,
    DEFAULT_LDAP_URI,
    DEFAULT_PORT,
    DEFAULT_SOLR_URL,
    USER_DN_TEMPLATE,
)
import logging, argparse


def add_logging_argparse_options(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    '''Add logging options to the given `parser`.'''
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-d',
        '--debug',
        action='store_const',
        const=logging.DEBUG,
        default=logging.INFO,
        dest='loglevel',
        help='Log copious debugging messages suitable for developers',
    )
    group.add_argument(
        '-q',
        '--quiet',
        action='store_const',
        const=logging.WARNING,
        dest='loglevel',
        help="Don't log anything except warnings and critically-important messages",
    )
    return parser


def add_argparse_options(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    '''Add the regular set of expected options (logging, version, solr, LDAP).'''

    # First, add the `--version` option
    parser.add_argument('--version', action='version', version=VERSION)

    # Now logging
    add_logging_argparse_options(parser)

    # HTTPS listen port
    parser.add_argument(
        '-p', '--port', metavar='N', type=int, default=DEFAULT_PORT,
        help='HTTPS listen port (default %(default)s)',
    )

    # Solr URL
    parser.add_argument(
        '-s', '--solr', metavar='URL', default=DEFAULT_SOLR_URL, help='Solr URL (default %(default)s)'
    )

    # LDAP
    parser.add_argument(
        '--ldap-uri', metavar='URI', default=DEFAULT_LDAP_URI,
        help='LDAP server URI for /imaging authentication (default %(default)s)',
    )
    parser.add_argument(
        '--ldap-group-dn', metavar='DN', default=DEFAULT_GROUP_DN,
        help='Group DN for access; user must be a `uniqueMember` of this group (default %(default)s)',
    )
    parser.add_argument(
        '--ldap-user-dn-template',
        metavar='TEMPLATE',
        default=USER_DN_TEMPLATE,
        help='Bind DN template with {username} placeholder (default %(default)s)',
    )
    parser.add_argument(
        '--subpath',
        metavar='PATH',
        default='',
        help='URL path prefix when running behind a reverse proxy (example: /infosphere)',
    )
    return parser
