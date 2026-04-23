# encoding: utf-8

'''🧠 LabCAS Infosphere: HTTPS ASGI application (Starlette).'''

from __future__ import annotations

import base64, binascii, csv, io, json, logging
from datetime import datetime, timezone
from importlib.resources import files

from starlette.applications import Starlette
from starlette.concurrency import run_in_threadpool
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, Response
from starlette.routing import Route

from ._imaging import imaging_report
from .const import DEFAULT_GROUP_DN, DEFAULT_LDAP_URI, DEFAULT_SOLR_URL, USER_DN_TEMPLATE
from . import ldap as ldap_auth

_BASIC_REALM = 'LabCAS Infosphere'
_logger = logging.getLogger(__name__)

def _www_authenticate() -> str:
    '''Return the HTTP Basic auth challenge header value.'''
    return f'Basic realm="{_BASIC_REALM}"'


def _parse_basic_credentials(request: Request) -> tuple[str, str] | None:
    '''Extract and decode Basic auth credentials from a request.'''
    auth = request.headers.get('Authorization')
    if auth is None or not auth.startswith('Basic '):
        return None
    try:
        raw = base64.b64decode(auth[6:].encode('ascii'), validate=True)
    except (binascii.Error, UnicodeError):
        return None
    if b':' not in raw: return None
    user, _, password = raw.partition(b':')
    try:
        return user.decode('utf-8'), password.decode('utf-8')
    except UnicodeDecodeError:
        return None


def _normalize_solr_url(url: str) -> str:
    '''Ensure the Solr base URL ends with a trailing slash.'''
    return url if url.endswith('/') else url + '/'


def _report_rows(report: dict[str, dict[str, dict[str, str]]]) -> list[dict[str, str]]:
    '''Flatten the imaging report into sorted row dictionaries.'''
    rows: list[dict[str, str]] = []
    for collection in sorted(report.keys()):
        for site in sorted(report[collection].keys()):
            for event in sorted(report[collection][site].keys()):
                rows.append({
                    'collection': collection,
                    'site': site,
                    'event': event,
                    'participantId': report[collection][site][event],
                })
    return rows


def _report_csv(report: dict[str, dict[str, dict[str, str]]]) -> str:
    '''Serialize the imaging report to CSV text.'''
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(['collection', 'site', 'event', 'participantId'])
    for collection in sorted(report.keys()):
        for site in sorted(report[collection].keys()):
            for event in sorted(report[collection][site].keys()):
                writer.writerow([collection, site, event, report[collection][site][event]])
    return buf.getvalue()


def _report_json(report: dict[str, dict[str, dict[str, str]]]) -> str:
    '''Serialize the imaging report rows to pretty-printed JSON.'''
    rows = _report_rows(report)
    return json.dumps(rows, indent=4) + '\n'


def _postman_collection_bytes() -> bytes:
    '''Read the packaged Postman collection JSON bytes.'''
    return files('jpl.labcas.infosphere').joinpath('resources/postman_collection.json').read_bytes()


def create_app(
    ldap_uri: str = DEFAULT_LDAP_URI,
    group_dn: str = DEFAULT_GROUP_DN,
    user_dn_template: str = USER_DN_TEMPLATE,
    solr_url: str | None = None,
    client_secret: str | None = None,
) -> Starlette:
    '''Build and configure the Starlette ASGI application.'''
    solr_base = _normalize_solr_url(solr_url or DEFAULT_SOLR_URL)

    # Health check endpoint
    async def ping(_request: Request) -> JSONResponse:
        '''Return a UTC timestamp used for health checks.'''
        return JSONResponse({'datetime': datetime.now(timezone.utc).isoformat()})

    # Imaging report endpoint
    async def imaging(request: Request) -> JSONResponse | Response:
        '''Authenticate the user and return the imaging report in JSON or CSV.'''
        parsed = _parse_basic_credentials(request)
        if parsed is None:
            return JSONResponse(
                {'detail': 'Not authenticated'},
                status_code=401,
                headers={'WWW-Authenticate': _www_authenticate()},
            )
        username, password = parsed
        _logger.info('Handling imaging request for user: %s', username)
        bind_dn = ldap_auth.user_dn(username, user_dn_template)
        ok = await run_in_threadpool(
            ldap_auth.authenticate_and_in_group,
            ldap_uri,
            bind_dn,
            password,
            group_dn,
        )
        if not ok:
            return JSONResponse(
                {'detail': 'Not authenticated'},
                status_code=401,
                headers={'WWW-Authenticate': _www_authenticate()},
            )
        report = await run_in_threadpool(imaging_report, solr_base, client_secret)
        fmt = request.query_params.get('format', 'json')
        if fmt == 'json':
            body = _report_json(report)
            return Response(body, media_type='application/json; charset=utf-8')
        if fmt == 'csv':
            body = _report_csv(report)
            return Response(body, media_type='text/csv; charset=utf-8')
        return JSONResponse({'detail': f'Invalid format: {fmt!r}'}, status_code=400)

    # API docs endpoint
    async def docs_home(request: Request) -> HTMLResponse:
        '''Return a simple docs landing page.'''
        root_path = request.scope.get('root_path', '').rstrip('/')
        postman_path = request.url_path_for('postman_collection')
        postman_url = str(
            request.url.replace(
                path=f'{root_path}{postman_path}',
                query='',
                fragment='',
            )
        )
        body = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>LabCAS Infosphere API Docs</title>
  </head>
  <body>
    <h1>LabCAS Infosphere API Docs</h1>
    <p>Import the Postman collection from this URL:</p>
    <p><a href="{postman_url}">{postman_url}</a></p>
  </body>
</html>
'''
        return HTMLResponse(body)

    # API docs endpoint
    async def postman_collection(_request: Request) -> Response:
        '''Return the packaged Postman collection JSON.'''
        return Response(
            _postman_collection_bytes(),
            media_type='application/json; charset=utf-8',
            headers={'Content-Disposition': 'inline; filename="postman_collection.json"'},
        )

    return Starlette(
        routes=[
            Route('/ping', endpoint=ping, methods=['GET']),
            Route('/imaging', endpoint=imaging, methods=['GET']),
            Route('/docs', endpoint=docs_home, methods=['GET']),
            Route('/docs/postman-collection', endpoint=postman_collection, methods=['GET'], name='postman_collection'),
        ],
    )


app = create_app()
