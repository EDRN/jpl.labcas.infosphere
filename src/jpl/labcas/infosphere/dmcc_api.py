# encoding: utf-8

'''🧠 LabCAS Infosphere: DMCC API.'''


from .const import DMCC_TOKEN_API, DMCC_IMAGE_EVENTS
import requests
from collections import defaultdict
from pprint import pprint


def dmcc_authenticate(client_id: str, client_secret: str) -> str:
    '''Authenticate to the DMCC's token API with a given client ID and secret, returning a
    bearer token.
    '''
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(DMCC_TOKEN_API, data=data, headers=headers)
    response.raise_for_status()
    return response.json().get('access_token')


def get_image_events(protocol_id: int, token: str):
    '''Retrieve all image events from the DMCC's image event API.
    
    Returns a dictionary of image event identifiers to dictionaries of event details.
    For example, the return value for protocol ID 354 might look like:
    {
        '1234567890': {
            'blindedId': '9340923',
            'imageTypeText': 'MRI',
            'participantId': '9341234991',
            'protocolId': '354',
            'siteId': '934',
            'visitTypeText': 'Baseline',
        }
        …
    }
    '''
    headers = {'Authorization': f'Bearer {token}'}
    params = {'protocolId': protocol_id}
    response = requests.get(DMCC_IMAGE_EVENTS, headers=headers, params=params)
    records = response.json()['imagingEventRecords']

    grouped: dict[str, dict[str, str]] = defaultdict(dict)

    for record in records:
        event_identifier = str(record.get('imageEventIdentifier', ''))
        if not event_identifier: continue
        grouped[event_identifier] = {
            'blindedId': record.get('blindedId'),
            'imageTypeText': record.get('imageTypeText'),
            'participantId': record.get('participantId'),
            'protocolId': record.get('protocolId'),
            'siteId': record.get('siteId'),
            'visitTypeText': record.get('visitTypeText'),
        }

    return grouped


if __name__ == '__main__':
    import os
    from .const import DMCC_CLIENT_ID, PROTOCOL_IDS
    token = dmcc_authenticate(DMCC_CLIENT_ID, os.getenv('DMCC_CLIENT_SECRET'))
    for protocol_id in PROTOCOL_IDS.values():
        image_events = get_image_events(protocol_id, token)
        pprint(image_events)
