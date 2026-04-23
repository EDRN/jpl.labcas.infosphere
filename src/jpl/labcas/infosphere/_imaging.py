# encoding: utf-8

'''🧠 LabCAS Infosphere: imaging report.'''

import pysolr, logging, collections
from .solr import site_events_by_pivot_facet
from .dmcc_api import dmcc_authenticate, get_image_events
from .const import DMCC_CLIENT_ID, PROTOCOL_IDS
from pprint import pprint

_logger = logging.getLogger(__name__)



def imaging_report(solr_url: str, client_secret: str) -> dict[str, dict[str, dict[str, str]]]:
    '''Generate an imaging report from the given Solr URL.
    
    The solr_url better end with a slash.
    The client_secret is used to authenticate with the DMCC API.
    '''
    token = dmcc_authenticate(DMCC_CLIENT_ID, client_secret)
    _logger.debug('Authenticated with DMCC API, received token of length %d', len(token))
    report: dict[str, dict[str, dict[str, str]]] = collections.defaultdict(lambda: collections.defaultdict(dict))
    solr = pysolr.Solr(solr_url + 'files', verify=False)
    _logger.debug('Connected to Solr at %s', solr_url + 'files')
    for collection_name, protocol_id in PROTOCOL_IDS.items():
        _logger.debug('Pivot-facet query for collection: %s', collection_name)
        pairs = site_events_by_pivot_facet(solr, f'CollectionId:{collection_name}')
        _logger.debug('Pivot-facet query for collection: %s returned %d pairs', collection_name, len(pairs))
        dmcc_imaging_events = get_image_events(protocol_id, token)
        _logger.debug('Retrieved %d imaging events from DMCC API for protocol ID %d', len(dmcc_imaging_events), protocol_id)
        for site_id, events in pairs.items():
            _logger.debug('Processing site: %s with %d events', site_id, len(events))
            for event_id in events:
                event_data = dmcc_imaging_events.get(event_id)
                if event_data is None:
                    _logger.warning('No imaging event data found for event ID: %s', event_id)
                    continue
                participant_id = event_data.get('participantId')
                if participant_id is None:
                    _logger.warning('No participant ID found for event ID: %s', event_id)
                    continue
                report[collection_name][site_id][event_id] = participant_id
                _logger.debug('Added participant ID %s for event ID %s to report', participant_id, event_id)
    _logger.debug('Report generated with %d collections, %d sites, and %d events', len(report), len(report[collection_name]), len(report[collection_name][site_id]))
    return report


if __name__ == '__main__':
    import os
    report = imaging_report('https://localhost:8984/solr/', os.getenv('DMCC_CLIENT_SECRET'))
    pprint(report)
