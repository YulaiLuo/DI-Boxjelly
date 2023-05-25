#!/bin/bash

# Start the Docker container
docker-compose up -d

# Wait for the ontoserver container to fully start
# You may need to adjust the sleep duration based on when your application is ready
sleep 30

# Run the command in the ontoserver container
sudo docker exec di-ontoserver /index.sh -s sctau
