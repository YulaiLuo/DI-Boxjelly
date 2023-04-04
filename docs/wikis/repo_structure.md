# Repository Structure

## Ansible files

    .
    ├── ...
    ├── ansible                   
    │   ├── roles           # ansible roles        
    │   ├── vars            # ansible scripts configurations
    │   ├── dev_inventory       # development infrastructure configurations
    │   └── dev_playbook.yaml   # ansible playbook develop on the development server
    └── ...

## Data samples

    .
    ├── ...
    ├── data samples                   
    │   └── ReasonExample.txt   # inputs of the system providede by client
    └── ...

## Documentation files

    .
    ├── ...
    ├── docs                   
    │   ├── checklist   # check list of each sprint         
    │   ├── release notes   # the docs of release
    │   ├── Expected outcome.pdf   # The expected system sturcture  provided by client  
    │   └── <There will be more>
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
    │   ├── di-frontend      # frontend code    
    │   ├── di-gateway       # microservice gateway 
    │   ├── di-login         # microservice login 
    │   ├── di-ontoserver    # microservice ontoserver       
    │   └── di-...           # more service 
    └── ...

## Tests 

    .
    ├── ...
    ├── tests                   
    │   └── <There will be tests files>
    └── ...