# Repository Structure

## Data samples

    .
    ├── ...
    ├── data samples     
    │   ├── 50.csv          # This file include 50 SNOMED-CT code which equals to corresponding UIL code
    │   ├── Indications (AMS)_Australia_19.xlsx indication list samples         # Universal indication list
    │   └── ReasonExample.txt   # inputs of the system providede by client
    └── ...

## Documentation files

    .
    ├── ...
    ├── docs                   
    │   ├── checklist   # check list of each sprint     
    │   ├── confluence-page     # Contains the confluence page exported file for product documentation
    │   ├── wiki   # the additional documentes of this project
    │   │    └── <Markdown pages>
    │   ├── images   # the images which will be used in markdown files
    │   │    └── <image files>
    │   └── Expected outcome.pdf   # The expected system sturcture provided by client  
    └── ...

## Prototypes files

    .
    ├── ...
    ├── prototypes                   
    │   └── <The initial prototypes image in first sprint>
    └── ...

## Source code

    .
    ├── ...
    ├── src                   
    │   ├── di-web          # frontend code with nginx settings 
    │   ├── di-auth          # microservice authentication and authorization 
    │   ├── di-gateway      # microservice gateway 
    │   ├── di-map          # microservice map       
    │   └── di-center          # microservice center   
    └── ...

## Tests 

    .
    ├── ...
    ├── tests                   
    │   └── <Code pieces and tests files>
    └── ...