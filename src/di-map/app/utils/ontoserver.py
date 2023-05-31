import pandas as pd
import requests
import json
import os
import glob


def resource_exists(url):
    # Send a GET request to the FHIR server
    response = requests.get(url,
                            headers={'Content-Type': 'application/fhir+json'},
                            verify=False)
    # If the status code is 200, then the resource exists
    return response.status_code == 200 and response.json()["total"] > 0


def create_concepts_from_xlsx(file_path):
    # Read the xlsx file
    df = pd.read_excel(file_path)

    # Create the concepts
    concepts = []
    for index, row in df.iterrows():
        concept = {
            "code": index,
            "display": row['Indication']
        }
        concepts.append(concept)
    return concepts


def create_codesystem(concepts):
    # Create the CodeSystem resource
    codesystem = {
        "resourceType": "CodeSystem",
        "url": "http://localhost:8443/fhir/CodeSystem/uil",
        "name": "UIL",
        "status": "draft",
        "publisher": "DI-BoxJelly",
        "caseSensitive": False,
        "valueSet": "http://localhost:8443/fhir/ValueSet/uil",
        "content": "complete",
        "concept": concepts
    }

    # Convert the dictionary to a JSON string
    codesystem_json = json.dumps(codesystem)

    # Check if the CodeSystem resource already exists
    url = 'https://localhost:8443/fhir/CodeSystem?name=UIL'
    if resource_exists(url):
        # If it exists, use a PUT request to update it
        response = requests.put('https://localhost:8443/fhir/CodeSystem',
                                data=codesystem_json,
                                headers={
                                    'Content-Type': 'application/fhir+json'},
                                verify=False)
    else:
        # If it doesn't exist, use a POST request to create it
        response = requests.post('https://localhost:8443/fhir/CodeSystem',
                                 data=codesystem_json,
                                 headers={
                                     'Content-Type': 'application/fhir+json'},
                                 verify=False)
    return response


def create_valueset():
    # Create the ValueSet resource
    valueset = {
        "resourceType": "ValueSet",
        "url": "http://localhost:8443/fhir/ValueSet/uil",
        "name": "UIL",
        "publisher": "DI-BoxJelly",
        "status": "active",
        "experimental": False,
        "compose": {
            "include": [
                {
                    "system": "http://localhost:8443/fhir/CodeSystem/uil"
                }
            ]
        }
    }

    # Convert the dictionary to a JSON string
    valueset_json = json.dumps(valueset)

    # Check if the ValueSet resource already exists
    url = 'https://localhost:8443/fhir/ValueSet?name=UIL'
    if resource_exists(url):
        # If it exists, use a PUT request to update it
        response = requests.put('https://localhost:8443/fhir/ValueSet',
                                data=valueset_json,
                                headers={
                                    'Content-Type': 'application/fhir+json'},
                                verify=False)
    else:
        # If it doesn't exist, use a POST request to create it
        response = requests.post('https://localhost:8443/fhir/ValueSet',
                                 data=valueset_json,
                                 headers={
                                     'Content-Type': 'application/fhir+json'},
                                 verify=False)
    return response


def init_ontoserver(app):
    # Run the ontoserver containers
    os.system("docker-compose up -d")

    # Wait for the ontoserver to be ready
    os.system("sleep 15")

    # Define the path to your xlsx file
    # Get a list of all .xlsx files in the current directory
    xlsx_files = glob.glob('./*.xlsx')

    # Check if the list is not empty
    if xlsx_files:
        # Get the first file
        file_path = xlsx_files[0]
        print(f"Found file: {file_path}")
    else:
        print("No .xlsx files found in current directory.")

    # Create the concepts from the xlsx file
    concepts = create_concepts_from_xlsx(file_path)

    # Create the CodeSystem
    codesystem_response = create_codesystem(concepts)

    # Create the ValueSet
    valueset_response = create_valueset()
