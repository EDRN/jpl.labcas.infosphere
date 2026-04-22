# encoding: utf-8

'''🧠 LabCAS Infosphere: imaging report.'''

import pysolr, logging, collections
from .solr import site_events_by_pivot_facet

_logger = logging.getLogger(__name__)

_collections = ['Lung_Team_Project_2', 'Prostate_MRI']

def imaging_report(solr_url: str) -> dict[str, dict[str, set[str]]]:
    '''Generate an imaging report from the given Solr URL.
    
    The solr_url better end with a slash.
    '''
    report: dict[str, dict[str, set[str]]] = collections.defaultdict(lambda: collections.defaultdict(set))
    solr = pysolr.Solr(solr_url + 'files', verify=False)
    for collection in _collections:
        _logger.info('Pivot-facet query for collection: %s', collection)
        pairs = site_events_by_pivot_facet(solr, f'CollectionId:{collection}')
        for site_id, events in pairs.items():
            report[collection][site_id].update(events)
    return report
