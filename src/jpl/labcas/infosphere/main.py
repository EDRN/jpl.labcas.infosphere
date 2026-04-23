# encoding: utf-8

'''🧠 LabCAS Infosphere: the information API for the Laboratory Catalog and Archive Service'''

import argparse, getpass, logging, os, pysolr, sys, uvicorn
from .app import create_app
from .argparse import add_argparse_options
from .tls import create_self_signed_tls_files
from . import VERSION

_logger = logging.getLogger(__name__)


def _uvicorn_log_level(level: int) -> str:
    '''Convert a logging level to a uvicorn log level.'''
    name = logging.getLevelName(level)
    if isinstance(name, str): return name.lower()
    else: return 'info'


def main():
    '''Main entry point for the LabCAS Infosphere server.'''
    parser = argparse.ArgumentParser(
        description='🧠 LabCAS Infosphere: the information API for the Laboratory Catalog and Archive Service'
    )
    parser = add_argparse_options(parser)
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel, format='%(levelname)s %(message)s')

    # Get the DMCC client secret from the environment or prompt the user
    if not os.getenv('DMCC_CLIENT_SECRET'):
        client_secret = getpass.getpass('DMCC client secret: ').strip()
        if not client_secret:
            _logger.error('DMCC client secret was not provided')
            return -1
    else:
        client_secret = os.getenv('DMCC_CLIENT_SECRET')

    _logger.info('Starting LabCAS Infosphere v%s with Solr at %s', VERSION, args.solr)
    solr_url = args.solr if args.solr.endswith('/') else args.solr + '/'

    app = create_app(
        ldap_uri=args.ldap_uri,
        group_dn=args.ldap_group_dn,
        user_dn_template=args.ldap_user_dn_template,
        solr_url=solr_url,
        client_secret=client_secret,
    )
    cert_path, key_path = create_self_signed_tls_files()
    try:
        _logger.info('Listening for HTTPS on https://localhost:%s/', args.port)
        uvicorn.run(
            app, host='localhost', port=args.port, ssl_certfile=cert_path, ssl_keyfile=key_path,
            log_level=_uvicorn_log_level(args.loglevel),
        )
    finally:
        for path in (cert_path, key_path):
            try: os.unlink(path)
            except OSError: pass


if __name__ == '__main__':
    sys.exit(main())