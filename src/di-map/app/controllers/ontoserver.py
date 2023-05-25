import requests
from fuzzywuzzy import fuzz


def check_uil_with_ontoserver(texts):
    # Prepare the payload for the Ontoserver bundle expand API
    payload = {
        "resourceType": "Bundle",
        "type": "batch",
        "entry": []
    }

    # Add an entry for each text
    for text in texts:
        payload['entry'].append(
            {
                "resource": {
                    "resourceType": "Parameters",
                    "parameter": [
                        {
                            "name": "url",
                            "valueUri": "http://localhost:8443/fhir/ValueSet/uil"
                        },
                        {
                            "name": "count",
                            "valueInteger": 1
                        },
                        {
                            "name": "filter",
                            "valueString": text
                        }
                    ]
                },
                "request": {
                    "method": "POST",
                    "url": "/ValueSet/$expand"
                }
            }
        )

    # Make the request to the Ontoserver bundle expand API
    response = requests.post(
        "https://localhost:8443/fhir", json=payload, verify=False)

    # Check if the request was successful
    if response.status_code != 200:
        raise Exception('Failed to call Ontoserver bundle expand API')

    # Process the response
    data = {}
    for i, entry in enumerate(response.json().get('entry', [])):
        resource = entry.get('resource', {})
        expansion = resource.get('expansion', {})
        contains = expansion.get('contains', [{}])[0]

        if 'code' in contains and 'display' in contains:
            similarity = fuzz.ratio(texts[i], contains['display'])
            data[i] = {
                # now it's custom code by index instead of sct code
                'uil_code': contains['code'],
                'uil_name': contains['display'],
                'similarity': similarity/100
            }

    return data
