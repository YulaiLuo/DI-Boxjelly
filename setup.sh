#!/bin/bash

# Check if Docker is installed
if ! command -v docker &> /dev/null
then
    echo "Docker is not installed. Please install it and run this script again."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null
then
    echo "Docker Compose is not installed. Please install it and run this script again."
    exit 1
fi

# Check if Yarn is installed
if ! command -v yarn &> /dev/null
then
    echo "Yarn is not installed. Please install it and run this script again."
    exit 1
fi

# Run the first Docker Compose command
docker-compose -f ontoserver-docker-compose.yml up -d

# Run the second Docker Compose command
docker-compose up -d

# Navigate to the di-web directory
cd src/di-web || { echo "di-web directory not found"; exit 1; }

# Run the yarn commands
yarn install
yarn build