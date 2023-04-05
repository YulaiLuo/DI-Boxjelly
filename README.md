# SNOMED CT Diagnostic and Prescription Mapping Tool with Ontoserver Integration
[![Sprint Status](https://img.shields.io/badge/sprint2-dev-orange)](https://your_project_management_tool.com/sprint_details) 
![Status Status](https://img.shields.io/badge/user_stories-1/8-green)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![Code Coverage](https://img.shields.io/badge/coverage-10%-red)

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

Here we list the top-level directory of this repository

More details about the sub-directories can be found in docs directory [repository structure](./docs/wikis/repo_structure.md).

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


## Features
* Ontoserver Integration
* Text Processing and Analysis
* Mapping to Universal Indication List(UIL - a subset of SNOMED CT)
* Machine Learning and Continuous Improvement
* User-friendly Interface
* Multilingual Support

## Installation and deployment
1. Clone the repository:

    `git clone https://github.com/COMP90082-2023-SM1/DI-Boxjelly.git`

2. In the command line, go to the ansible directory

        cd ansible

3. Install the ansible requirments:

        ansible-galaxy install -r requirements.yml

4. Modify the inventory configuration in the *inventory.ini* file to the host your wanna deploy this system

5. Use ansible for auto-deployment:

        ansible-playbook -i inventory playbook.yaml


## Requirements

### Prerequisites

* You need to have the Ontoserver licsence which can be applied [here]().
* You need to have an account on [NCTS](https://www.healthterminologies.gov.au/) to get a client id and client secret which will be used to deploy a Ontoserver image.

### System requirments

| Resource      	| Minmum 	| Recommended 	|
|---------------	|--------	|-------------	|
| CPUs or Cores 	|   4     	|      8      	|
| RAM           	|   4G     	|     16G      	|
| Storage/Disk  	|   20G    	|     >=40G    	|

### Environment requirments
* Python 3.9+
* Docker  
Following the [offical docker installation](https://docs.docker.com/engine/install/ubuntu/)
* Ansible  
        
        pip install ansible  

    or  

        conda install ansible


## Usage  

Project preview: [Mapping](http://101.43.110.249:8000/map/ontoserver/translate?code=Tonsillitis)

### Login Page
![workflow](./docs/images/login.png)


### Main Page
![workflow](./docs/images/main_page.png)


## Project Workflow

Team members please follow the following version control convention and branch naming convention when developing code.

More detail how to follow the workflow please visits [workflow](./docs/wikis/workflow.md)


![workflow](./docs/images/workflow.jpg)




