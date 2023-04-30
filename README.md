# SNOMED CT Diagnostic and Prescription Mapping Tool with Ontoserver Integration
<!-- [![Sprint Status](https://img.shields.io/badge/sprint2-dev-orange)](https://your_project_management_tool.com/sprint_details)  -->
<!-- ![Status Status](https://img.shields.io/badge/user_stories-1/8-green) -->
![Python Version](https://img.shields.io/badge/python-v3.9.16%2B-blue)
![Python Version](https://img.shields.io/badge/flask-v2.2.2%2B-red)
![Python Version](https://img.shields.io/badge/react-v18.2.0%2B-red)
![Python Version](https://img.shields.io/badge/release-1.2.0%2B-green)

The primary objective of this project is to determine whether medications prescribed to patients are appropriate by normalizing free-text clinical notes and mapping them to canonical clinical terms.

The platform's primary function is to simplify the process of associating brief free-text descriptions, which generally explain the reasoning behind prescribing specific medications, onto a standardized knowledge base of clinical terms known as SNOMED CT.

The platform features the integration of a human-in-the-loop system, which allows for manual review and correction of the mapping results. This feedback will be used to continuously enhance the platform's accuracy and performance.

A key component of the platform is the development of a Universal Indication List (UIL), which serves as a subset of the broader SNOMED CT. This curated list will further streamline the mapping process, ensuring that the most relevant and commonly used clinical terms are easily accessible for healthcare professionals and researchers.

<!-- ![Code Coverage](https://img.shields.io/badge/coverage-10%-red) -->

<!-- ![License](https://img.shields.io/badge/license-MIT-green) -->

<!-- ![Build Status](https://img.shields.io/badge/build-passing-brightgreen) -->

<!-- ## Table of Contents
- [Background](#background)
- [Repository Structure](#repository-structure)
- [Features](#features)
- [Installation](#installation)
- [Requirements](#requirements)
- [Usage](#usage)
- [Workflow](#workflow)
- [License](#license) -->
 

## Repository Structure

Here we list the top-level directory of this repository

More details about the sub-directories can be found in docs directory [repository structure](./docs/wikis/repo_structure.md).

    .
    ├── ansible       # Automated deployment scripts
    ├── data samples  # Sample input for the prototype 
    ├── docs          # Documentation files  
    ├── prototypes    # Designed user interface - prototypes
    ├── src           # Source code
    ├── tests         # Code pieces and automated tests of source code
    ├── ui            # Designed UI
    ├── LICENSE       # <Not included for now>
    ├── README.md
    └── .gitignore

## Features
* Map clinical free text to Universal Indication List(UIL - a subset of SNOMED CT)
* Curate mapping result category
* Continuously improve mapping performance
* Download mapping result
* Collaborate with team members
* Rollback the system
* Data protection

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


## Demo and preview
A demo video is available at MedCAT, and the preview website is available at [here](http://101.43.110.249:8000/map/ontoserver/translate?code=Tonsillitis).
[![Watch the video](./docs/images/login.png)](https://www.youtube.com/watch?v=1i55TeItS0Q)


### Main Page
![workflow](./docs/images/main_page.png)


## Project Workflow

Team members follow the following version control convention and branch naming convention when developing code.

More detail how to follow the workflow please visits [workflow](./docs/wikis/workflow.md)


![workflow](./docs/images/workflow.jpg)




