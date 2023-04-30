# Repository Structure

## Ansible files

    .
    ├── ...
    ├── ansible                   
    │   ├── roles           # ansible roles        
    │   ├── vars            # ansible scripts configurations
    │   ├── local_deploy.yaml            # ansible playbook to deploy on local machine
    │   ├── localhost.ini            # deploy local configurations
    │   ├── tencent_cloud.ini       # development infrastructure configurations
    │   └── one_remote_playbook.yaml   # ansible playbook develop on the development server
    └── ...

## Data samples

    .
    ├── ...
    ├── data samples     
    │   ├── Indications (AMS)_Australia_19.xlsx indication list samples
    │   └── ReasonExample.txt   # inputs of the system providede by client
    └── ...

## Documentation files

    .
    ├── ...
    ├── docs                   
    │   ├── checklist   # check list of each sprint         
    │   ├── release notes   # the docs of release
    │   ├── wiki   # the additional documentation of project
    │   │    └── <Markdown pages>
    │   ├── images   # the images which will be used in markdown files
    │   │    └── <image files>
    │   └── Expected outcome.pdf   # The expected system sturcture  provided by client  
    └── ...

## Prototypes files

    .
    ├── ...
    ├── prototypes                   
    │   └── <There will be prototype images>
    └── ...

## Source code

    .
    ├── ...
    ├── src                   
    │   ├── di-web          # frontend code    
    │   ├── di-auth          # microservice authentication and authorization 
    │   ├── di-common       # microservice common services: email... 
    │   ├── di-gateway      # microservice login 
    │   ├── di-map          # microservice map       
    │   └── di-uil          # microservice UIL   
    └── ...

## Tests 

    .
    ├── ...
    ├── tests                   
    │   └── <There will be code pieces and tests files>
    └── ...