# encoding: utf-8

'''🧠 LabCAS Infosphere: Solr.'''

import pysolr, logging
from typing import Generator
from .const import SOLR_ROWS, SOLR_SORT

_logger = logging.getLogger(__name__)

# Pivot facet: return all distinct values (Solr default caps facet buckets).
_FACET_UNLIMITED = '-1'


def site_events_by_pivot_facet(
    solr: pysolr.Solr,
    query: str,
    site_field: str = 'BlindedSiteID',
    event_field: str = 'eventID',
) -> dict[str, set[str]]:
    '''Distinct (site, event) pairs for ``query`` via Solr pivot faceting.

    Requires ``site_field`` and ``event_field`` to be facetable in the Solr schema
    (typically string fields with ``docValues=true`` or legacy indexed terms).
    Uses ``rows=0`` so no document bodies are transferred.
    '''
    pivot_key = f'{site_field},{event_field}'
    results = solr.search(
        query, rows=0, facet='true',
        **{
            'facet.pivot': pivot_key,
            'facet.pivot.mincount': 1,
            'facet.limit': _FACET_UNLIMITED,
            # Nested pivot level defaults to a small limit unless overridden per field.
            f'f.{site_field}.facet.limit': _FACET_UNLIMITED,
            f'f.{event_field}.facet.limit': _FACET_UNLIMITED,
        },
    )
    facet_counts = results.facets or {}
    pivot = facet_counts.get('facet_pivot') or {}
    rows = pivot.get(pivot_key) or []
    out: dict[str, set[str]] = {}
    for entry in rows:
        site = entry.get('value')
        if site is None or site == '':
            continue
        site_s = str(site)
        for sub in entry.get('pivot') or []:
            ev = sub.get('value')
            if ev is None or ev == '':
                continue
            out.setdefault(site_s, set()).add(str(ev))
    return out


def find_documents(solr: pysolr.Solr, query: str, fields: list[str]) -> Generator[dict, None, None]:
    '''Find documents in Solr matching the given query and fields.'''

    # cursorMark + sort: pysolr follows nextCursorMark across pages when iterating Results.
    params: dict = {'rows': SOLR_ROWS, 'sort': SOLR_SORT, 'cursorMark': '*'}
    if fields: params['fl'] = ','.join(fields)
    results = solr.search(query, **params)
    if results.hits == 0: _logger.debug('No documents matched query %s', query)
    yield from results
