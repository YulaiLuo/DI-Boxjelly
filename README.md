# SNOMED CT Diagnostic and Prescription Mapping Tool with Ontoserver Integration
[![Sprint Status](https://img.shields.io/badge/sprint1-design-orange)](https://your_project_management_tool.com/sprint_details) 
![Status Status](https://img.shields.io/badge/user_stories-0/8-green)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![Code Coverage](https://img.shields.io/badge/code_coverage-0%-red)

<!-- ![License](https://img.shields.io/badge/license-MIT-green) -->

<!-- ![Build Status](https://img.shields.io/badge/build-passing-brightgreen) -->

## Table of Contents
- [Background](#background)
- [Repository Structure](#repository-structure)
- [Features](#features)
- [Installation](#installation)
- [Requirements](#requirements)
- [Usage](#usage)
- [Workflow](#workflow)
<!-- - [License](#license) -->
 
## Background
Our team is working on the development of a cutting-edge platform designed to enhance the analysis of clinical documentation in the digital health area. The primary objective of this platform is to determine whether medications prescribed to patients are appropriate by normalizing free-text clinical notes and mapping them to canonical clinical terms.

The platform's primary function is to simplify the process of associating brief free-text descriptions, which generally explain the reasoning behind prescribing specific medications, onto a standardized knowledge base of clinical terms known as SNOMED CT.

The platform features the integration of a human-in-the-loop system, which allows for manual review and correction of the mapping results. This feedback will be used to continuously enhance the platform's accuracy and performance.

A key component of the platform is the development of a Universal Indication List (UIL), which serves as a subset of the broader SNOMED CT. This curated list will further streamline the mapping process, ensuring that the most relevant and commonly used clinical terms are easily accessible for healthcare professionals and researchers.

## Repository Structure

### Top-level directory
    .
    ├── ansible       # Automated deployment scripts
    ├── data samples  # Sample input for the prototype 
    ├── docs          # Documentation files  
    ├── prototypes    # Designed user interface - prototypes
    ├── src           # Source code
    ├── tests         # Automated tests of source code
    ├── ui            # Designed UI
    ├── LICENSE       # <Not included for now>
    ├── README.md
    └── .gitignore

### Ansible files

    .
    ├── ...
    ├── ansible                   
    │   ├── roles           # ansible roles        
    │   ├── vars            # ansible scripts configurations
    │   ├── inventory       # infrastructure configurations
    │   └── playbook.yaml   # ansible playbook
    └── ...

### Data samples

    .
    ├── ...
    ├── data samples                   
    │   └── ReasonExample.txt   # inputs of the system providede by client
    └── ...

### Documentation files

    .
    ├── ...
    ├── docs                   
    │   ├── checklist   # check list of each sprint         
    │   ├── release notes   # the docs of release
    │   ├── Expected outcome.pdf   # The expected system sturcture  provided by client  
    │   └── <There will be more>
    └── ...

### Prototypes files

    .
    ├── ...
    ├── prototypes                   
    │   └── <There will be prototype images>
    └── ...

### Source code

    .
    ├── ...
    ├── src                   
    │   ├── di-frontend      # frontend code    
    │   ├── di-gateway       # microservice gateway 
    │   ├── di-login         # microservice login 
    │   ├── di-ontoserver    # microservice ontoserver       
    │   └── di-...           # more service 
    └── ...

### Tests 

    .
    ├── ...
    ├── tests                   
    │   └── <There will be tests files>
    └── ...

## Features
* Ontoserver Integration
* Text Processing and Analysis
* Mapping to Universal Indication List(UIL - a subset of SNOMED CT)
* Machine Learning and Continuous Improvement
* User-friendly Interface
* Multilingual Support

## Installation
1. Clone the repository:

    `git clone https://github.com/COMP90082-2023-SM1/DI-Boxjelly.git`

<!-- 2. Use ansible for auto-deployment:

    ansible-playbook -i inventory playbook.yaml -->


## Requirements

### Prerequisites

* You need to have the Ontoserver licsence which can be applied [here]().
* You need to have an account on [NCTS](https://www.healthterminologies.gov.au/) account to get a client id and client secret which will be used to deploy a Ontoserver image.

### System requirments

| Resource      	| Minmum 	| Recommended 	|
|---------------	|--------	|-------------	|
| CPUs or Cores 	|   4     	|      8      	|
| RAM           	|   4G     	|     16G      	|
| Storage/Disk  	|   20G    	|     >=20G    	|

### Environment requirments
* Python 3.9+
* Docker  
Following the [offical docker installation](https://docs.docker.com/engine/install/ubuntu/)
* Ansible  

        pip install ansible  
        or
        conda install ansible


## Usage  
  
(There will be usage description)


## Workflow

### Branches
The project follows a specific branching model to maintain a clean and organized repository:

1. `main` or `master`: The main branch represents the stable, production-ready version of the application. **Direct commits to this branch are not allowed.**
2. `develop`: The develop branch is used for make develop commits. It used to integrate features and bugfixes before they are merged into the main branch. It is checked out from main branch, and **it will not be merged into any other branch.**
3. `test`: The test branch is used by the tester to do testing which is checked out from the `develop` branch by the end of a sprint. After the testing is done, the tester give the feedback wheather it pass the tests, then the team decide to create a release branch. **Note that `test` branch will not be merged into other branch.**
4. `feature/<feature name>`: Feature branches are created for each new feature or enhancement. They should be named `feature/login` for login feature. It is checked out from the `develop` branch.
5. `fix/<bug name>`: Bug branches are created for fixing bugs and issues. It is followed by the bug name or issue id, for example: `fix/issue202`. They should based on the `develope` branch, and sometimes it is checked out from main branch for emergency hotfix.
6. `release/<version number>`: Release branches are created for preparing new releases which follow by version number, such as `release/v1.0.0`. They are checked out from the `develop` branch. After the release is complete, developer make a pull request to the QA which will be merged into `main` branch with tag, and then be deleted.

### Naming Conventions
1. Branch names: Use lowercase letters and separate words with hyphens (e.g., feature/new-feature).
2. Commit messages: Write concise and descriptive commit messages, starting with a capital letter and using the imperative mood (e.g., 'Add new feature' or 'Fix bug in feature').
3. Style guid: 
    - Python: [Google python style guide](https://google.github.io/styleguide/pyguide.html)
    - Javascript: [Google JavaScript Style Guide](https://google.github.io/styleguide/jsguide.html
)

### Pull Requests and Code Review
When a feature or bugfix is complete, submit a pull request to the develop branch.
Request a code review from a team member.
Address any comments or requested changes.
After approval, merge the pull request into the develop branch and delete the feature or bugfix branch.
