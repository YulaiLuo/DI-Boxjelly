# SNOMED CT Diagnostic and Prescription Mapping Tool
<!-- [![Sprint Status](https://img.shields.io/badge/sprint2-dev-orange)](https://your_project_management_tool.com/sprint_details)  -->
<!-- ![Status Status](https://img.shields.io/badge/user_stories-1/8-green) -->

![Python Version](https://img.shields.io/badge/python-v3.9.16%2B-blue)
![Python Version](https://img.shields.io/badge/flask-v2.2.2%2B-red)
![Python Version](https://img.shields.io/badge/react-v18.2.0%2B-red)
<!-- ![web workflow](https://github.com/github/docs/actions/workflows/deploy_web.yml/badge.svg) -->

<!-- ![Code Coverage](https://img.shields.io/badge/coverage-10%-red) -->

<!-- ![License](https://img.shields.io/badge/license-MIT-green) -->

<!-- ![Build Status](https://img.shields.io/badge/build-passing-brightgreen) -->

## Table of Contents
- [SNOMED CT Diagnostic and Prescription Mapping Tool](#snomed-ct-diagnostic-and-prescription-mapping-tool)
	- [Table of Contents](#table-of-contents)
	- [Background](#background)
	- [Repository Structure](#repository-structure)
	- [Features](#features)
	- [Requirements](#requirements)
		- [System requirments](#system-requirments)
		- [Prerequisites (for Windows Server 2019)](#prerequisites-for-windows-server-2019)
		- [Prerequisites (for Ubuntu Linux)](#prerequisites-for-ubuntu-linux)
		- [Prerequisites (for macOS)](#prerequisites-for-macos)
		- [Ontoserver Setup and Licensing](#ontoserver-setup-and-licensing)
		- [MedCAT Model Setup](#medcat-model-setup)
	- [Installation and deployment](#installation-and-deployment)
	- [Website Demo](#website-demo)
	- [Website Preview](#website-preview)
		- [Login:](#login)
		- [Dashboard:](#dashboard)
		- [Team Management](#team-management)
		- [Invite Members](#invite-members)
		- [Code System](#code-system)
		- [Map Task](#map-task)
		- [Map Result](#map-result)
		- [Map Result Visualisation](#map-result-visualisation)
		- [Curation](#curation)
	- [Project Workflow](#project-workflow)

## Background

The primary objective of this platform is to determine whether medications prescribed to patients are appropriate by normalizing free-text clinical notes and mapping them to canonical clinical terms.

The platform's primary function is to simplify the process of associating brief free-text descriptions, which generally explain the reasoning behind prescribing specific medications, onto a Universal Indication List (UIL), which serves as a subset of the broader standardized knowledge base of clinical terms known as SNOMED CT.

The platform features the integration of a human-in-the-loop system, which allows for manual review and correction of the mapping results. This feedback will be used to continuously enhance the platform's accuracy and performance.

This curation feature will further streamline the mapping process, ensuring that the most relevant and commonly used clinical terms are easily accessible for healthcare professionals and researchers.

## Repository Structure

Here we list the top-level directory of this repository

More details about the sub-directories can be found in docs directory [repository structure](./docs/wikis/repo_structure.md).

	.
	├── .github       # CI/CD Github Action scripts
	├── data samples  # Sample input for the prototype
	├── docs          # Documentation files
	├── prototypes    # Designed user interface - prototypes
	├── src           # Source code
	├── tests         # Code pieces and tests of source code
	├── LICENSE       # <Not included for now>
	├── docker-compose.yml  # deploy other services exclude ontoserver
	├── ontoserver-docker-compose.yml   # deploy ontoserver
	├── README.md
	└── .gitignore

## Features

- Map: Translate clinical texts to Universal Indication List and SNOMED-CT
- Curate: Manually map result category to continuously improve mapping performance
- Visulization: Mapping result visulization
- Download: Export the mapping result
- Dashboard: System performance visulization
- Team: Member management
- Code system: Update code system version

## Requirements

### System requirments

| Resource      | Minmum | Recommended |
| ------------- | ------ | ----------- |
| CPUs or Cores | 4      | 8           |
| RAM           | 8G     | 16G         |
| Storage/Disk  | 20G    | >=40G       |

### Prerequisites (for Windows Server 2019)
Ensure that the following software is installed:

1. Windows Subsystem for Linux (WSL): Follow the [official Microsoft WSL Installation Guide](https://learn.microsoft.com/en-us/windows/wsl/install).

2. Docker: Download [Docker for Windows](https://docs.docker.com/desktop/install/windows-install/) from the Docker website and install it.

3. Docker Compose: Docker Compose is included in the Docker Desktop installation package.

4. Node.js and Yarn: Download and install Node.js from the [official Node.js website](https://nodejs.org/en/download). After installing Node.js, install Yarn by following the instructions on the [Yarn website](https://classic.yarnpkg.com/en/docs/install/#windows-stable).

Ensure that you select the option to use WSL 2 as the default when installing Docker.

### Prerequisites (for Ubuntu Linux)
Ensure that the following software is installed:

1. Docker: Follow the official [Docker installation guide for Ubuntu](https://docs.docker.com/engine/install/ubuntu/) to install it.

2. Docker Compose: After Docker is installed, follow the [Docker Compose installation guide](https://docs.docker.com/compose/install/).

3. Node.js and Yarn: Download and install Node.js and Yarn by unning the following commands in the terminal:

		sudo apt update
		sudo apt install nodejs
		sudo apt install npm
		npm install --global yarn

### Prerequisites (for macOS)
Ensure that the following software is installed:

1. Docker: Download Docker Desktop for Mac from the [Docker website](https://docs.docker.com/desktop/install/mac-install/) and install it.

2. Docker Compose: Docker Compose is included in the Docker Desktop installation package.

3. Node.js and Yarn: Download and install Node.js from the [official Node.js website](https://nodejs.org/en/download). After installing Node.js, install Yarn by following the instructions on the [Yarn website](https://classic.yarnpkg.com/lang/en/docs/install/#mac-stable).

### Ontoserver Setup and Licensing
- Root permission required
- Ontoserver license:
- Within Australia, email help@digitalhealth.gov.au to request a (free) Ontoserver licence. ADHA will then arrange authorisation for your quay.io account
- Elsewhere, email ontoserver-support@csiro.au to discuss licensing terms (both evaluation and production licences are available for single and multiple instances with no limit on the number of users). Once the licence is established, CSIRO will register your quay.io account name to enable access to their repository
- Note: The license is provided for either individual or organisation. University of Melbourne holds an active license, if you would like to use the license from Unimelb, please contact who is responsible for the Ontoserver license at Unimelb.
- Once you have a license and have access to the Ontoserver image on quay.io, remember to change the `CLIENT_ID` and `CLIENT_SECRET` in the `docker-compose.yml`. For information on how to retrieve these credentials, please consult the [Ontoserver documentation](https://ontoserver.csiro.au/docs/6.1/config-syndication.html#Australian_NCTS_Syndication).
![](./docs/images/ontoserver-docker-compose.jpg)
- Ensure your dockerhub account has been registered with ontoserver-support@csiro.au
- Docker login to quay.io required
![](./docs/images/docker-login1.png)
![](./docs/images/docker-login2.png)

### MedCAT Model Setup
1. Download the model by [following this link](https://uts.nlm.nih.gov/uts/login?service=https://medcat.rosalind.kcl.ac.uk/auth-callback) and sign into your NIH profile / UMLS license. 
2. You will then be redirected to the MedCAT model download form. Please complete the form and you will be provided a download link.
3. Unzip the downloaded model, rename the folder as `medtcat_model` and move the folder under `di-map` folder.

Ensure that you select the option to use model of SNOMED International (Full SNOMED modelpack trained on MIMIC-III).

## Installation and deployment

1. Clone the repository:

		git clone https://github.com/COMP90082-2023-SM1/DI-Boxjelly.git

2. Navigate into the cloned repository:

		cd DI-Boxjelly

3. Run the setup script:

		sudo ./setup.sh

	The setup script automates the installation and deployment process, including the deployment of the Ontoserver service and other services. If you prefer to run the script, proceed with this step. Otherwise, you can proceed with alternative manual deployment from step 4 to step 5.

4. Run the following command to deploy all services.

		docker-compose up -d

	Note:
	- This allows you to have 7 containers: mongodb, di-gateway, di-auth, di-center, di-map, nginx, ontoserver and ontoserver-db.
	- However, we did not automate the di-web set up, so you will need to manully build the web static file, and move the file to the instance. Though we do have a Dockerfile *src/di-web*, it is not a good choice for CI/CD, because the nginx container bind the HTML files locally on the instance. Therefore, to make it faster for CI/CD, we decide to manully set up the di-web module at the first set-up.

5. Set up the web, and nginx condiguration. In **src/di-web**, run the following command:

		yarn install
		yarn build

## Website Demo

A demo video is available:
[![Watch the video](./docs/images/login.png)](https://youtu.be/BC8NPPdGJ6M)

## Website Preview

You can access the production environment at [http://115.146.95.215](http://115.146.95.215)

### Login:
![workflow](./docs/images/login.png)

### Dashboard:
![workflow](./docs/images/dashboard.png)

### Team Management
![workflow](./docs/images/team-member.png)

### Invite Members
![workflow](./docs/images/invite-member.png)

### Code System
![workflow](./docs/images/code-system.png)

### Map Task
![workflow](./docs/images/map-tasks.png)

### Map Result
![workflow](./docs/images/map-result.png)

### Map Result Visualisation
![workflow](./docs/images/visualisation.png)

### Curation
![workflow](./docs/images/curate.png)

## Project Workflow

Team members follow the following version control convention and branch naming convention when developing code.

More detail how to follow the workflow please visits [workflow](./docs/wikis/workflow.md).

![workflow](./docs/images/workflow.jpg)
