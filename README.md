# SNOMED CT Diagnostic and Prescription Mapping Tool with Ontoserver Integration
[![Sprint Status](https://img.shields.io/badge/sprint-1-orange)](https://your_project_management_tool.com/sprint_details)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Code Coverage](https://img.shields.io/badge/coverage-95%25-green)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
<!-- ![License](https://img.shields.io/badge/license-MIT-green) -->


The SNOMED CT Diagnostic and Prescription Mapping Tool is a software solution designed to streamline the conversion of short diagnoses and prescriptions into their corresponding SNOMED CT codes using the power of Ontoserver and similar tools. SNOMED CT (Systematized Nomenclature of Medicine - Clinical Terms) is a comprehensive, multilingual clinical healthcare terminology that provides a standardized and consistent way to represent clinical information.

Ontoserver is a terminology server that supports various standardized terminologies, including SNOMED CT. This project leverages the capabilities of Ontoserver to provide accurate mappings for diagnoses and prescriptions.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Workflow](#workflow)
- [Contributing](#contributing)
- [License](#license)

## Features
* Ontoserver Integration
* Text Processing and Analysis
* Mapping to SNOMED CT Codes
* Machine Learning and Continuous Improvement
* User-friendly Interface
* Integration with EHR Systems
* Multilingual Support

## Requirements
* Python 3.9+
* Docker
* Ansible
* Flask
* React
* Ontoserver or a similar terminology server

## Installation
1. Clone the repository:

    `git clone https://github.com/your_username/SNOMED_CT_Mapping_Tool.git`



2. Install the required packages:

    `pip install -r requirements.txt`


3. Set up Ontoserver or a similar terminology server following the provider's guidelines.

## Usage
1. Configure the integration with Ontoserver or a similar terminology server in the application settings.

2. Run the Flask server:
pip install -r requirements.txt


3. Set up Ontoserver or a similar terminology server following the provider's guidelines.

## Usage
1. Configure the integration with Ontoserver or a similar terminology server in the application settings.

2. Run the Flask server:
python app.py


3. Open the web browser and navigate to `http://localhost:5000` to access the user interface.

4. Input short diagnoses and prescriptions and receive the corresponding SNOMED CT codes in real-time.

## Workflow

### Branches
The project follows a specific branching model to maintain a clean and organized repository:

1. `main`: The main branch represents the stable, production-ready version of the application. Direct commits to this branch are not allowed.
2. `sprint1develop`: The develop branch is used for integrating features and bugfixes before they are merged into the main branch. All feature and bugfix branches should be based on this branch and merged back into it after they have been reviewed and tested.
3. `feature/*`: Feature branches are created for each new feature or enhancement. They should be named `feature/feature_name` and based on the develop branch.
4. `bugfix/*`: Bugfix branches are created for fixing bugs and issues. They should be named `bugfix/bug_name` and based on the develop branch.
5. `release/*`: Release branches are created for preparing new releases. They should be named `release/version_number` and based on the develop branch. After the release is complete, the branch should be merged into both the main and develop branches, and then deleted.

### Naming Conventions
1. Branch names: Use lowercase letters and separate words with hyphens (e.g., feature/new-feature).
2. Commit messages: Write concise and descriptive commit messages, starting with a capital letter and using the imperative mood (e.g., 'Add new feature' or 'Fix bug in feature').
3. Variable and function names: Follow the PEP 8 style guide for Python code, using snake_case for variables and functions, and CamelCase for class names.

### Pull Requests and Code Review
When a feature or bugfix is complete, submit a pull request to the develop branch.
Request a code review from a team member.
Address any comments or requested changes.
After approval, merge the pull request into the develop branch and delete the feature or bugfix branch.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Simply create a new file named `README.md` and paste the above content into it. This will display the README file in your project repository in Markdown format.
