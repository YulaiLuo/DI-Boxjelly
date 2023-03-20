# SNOMED CT Diagnostic and Prescription Mapping Tool with Ontoserver Integration
[![Sprint Status](https://img.shields.io/badge/sprint1-design-orange)](https://your_project_management_tool.com/sprint_details) 
![Status Status](https://img.shields.io/badge/user_stories-0/8-green)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
<!-- ![License](https://img.shields.io/badge/license-MIT-green) -->
<!-- ![Code Coverage](https://img.shields.io/badge/coverage-95%25-green) -->
<!-- ![Build Status](https://img.shields.io/badge/build-passing-brightgreen) -->

Our team is working on the development of a cutting-edge platform designed to enhance the analysis of clinical documentation in the digital health area. The primary objective of this platform is to determine whether medications prescribed to patients are appropriate by normalizing free-text clinical notes and mapping them to canonical clinical terms.

The platform's primary function is to simplify the process of associating brief free-text descriptions, which generally explain the reasoning behind prescribing specific medications, onto a standardized knowledge base of clinical terms known as SNOMED CT.

The platform features the integration of a human-in-the-loop system, which allows for manual review and correction of the mapping results. This feedback will be used to continuously enhance the platform's accuracy and performance.

A key component of the platform is the development of a Universal Indication List (UIL), which serves as a subset of the broader SNOMED CT. This curated list will further streamline the mapping process, ensuring that the most relevant and commonly used clinical terms are easily accessible for healthcare professionals and researchers.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Workflow](#workflow)
<!-- - [License](#license) -->

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
<!-- * Docker
* Ansible
* Flask
* React -->
* Ontoserver or a similar terminology server

## Installation
1. Clone the repository:

    `git clone https://github.com/COMP90082-2023-SM1/DI-Boxjelly.git`

2. Install the required packages:

    <!-- `pip install -r requirements.txt` -->

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
2. `dev/sprint<number>`: The develop branch is used for integrating features and bugfixes before they are merged into the main branch. All feature and bugfix branches should be based on this branch and merged back into it after they have been reviewed and tested.
3. `feature/<feature name>`: Feature branches are created for each new feature or enhancement. They should be named `feature/login` for example, and based on the `dev/sprint<number>` branch.
4. `bug/<bug name>`: Bug branches are created for fixing bugs and issues. They should based on the `dev/sprint<number>` branch.
5. `release/<version number>`: Release branches are created for preparing new releases. They should based on the `dev/sprint<number>` branch. After the release is complete, the branch should be merged into both the main and develop branches, and then deleted.

### Naming Conventions
1. Branch names: Use lowercase letters and separate words with hyphens (e.g., feature/new-feature).
2. Commit messages: Write concise and descriptive commit messages, starting with a capital letter and using the imperative mood (e.g., 'Add new feature' or 'Fix bug in feature').
3. Style guid: 
    - Python: Use [Google python style guide](https://google.github.io/styleguide/pyguide.html) to write code

### Pull Requests and Code Review
When a feature or bugfix is complete, submit a pull request to the develop branch.
Request a code review from a team member.
Address any comments or requested changes.
After approval, merge the pull request into the develop branch and delete the feature or bugfix branch.

Test