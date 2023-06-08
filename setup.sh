#!/bin/bash

# Check if Docker is installed
if ! command -v docker &> /dev/null
then
    echo "Docker is not installed. Please install it and run this script again."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! command -v docker-compose-plugin &> /dev/null
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

# Navigate to the di-web directory
cd src/di-web || { echo "di-web directory not found"; exit 1; }

# Run the yarn commands
yarn install
yarn build

# Check if the build directory exists
if [ ! -d "build" ]
then
    echo "Build directory does not exist. Please check if the build command succeeded."
    exit 1
fi

# Create the necessary directories
mkdir -p ~/data/di-data/nginx/conf
mkdir -p ~/data/di-data/nginx/html
mkdir -p ~/data/di-data/nginx/ssl
mkdir -p ~/data/di-data/nginx/logs
mkdir -p ~/data/di-data/di-auth/avatars
mkdir -p ~/data/di-data/di-map/medcat_model

# Copy nginx configuration file in the di-web directory to the desired location
cp -r nginx.conf ~/data/di-data/nginx/conf/ || { echo "Failed to copy files from the di-web directory."; exit 1; }

# Copy all files in the build directory to the desired location
cp -r build/* ~/data/di-data/nginx/html/ || { echo "Failed to copy files from the build directory."; exit 1; }

# Navigate back to the root directory
cd ../..

# Copy the medcat model folder to the desired location
cp -r src/di-map/medcat_model/* ~/data/di-data/di-map/medcat_model/ || { echo "Failed to copy files from the medcat_model directory. Please ensure you unzip the downloaded model, rename the folder as medcat_model and move it under di-map folder."; exit 1; }

# Copy the default avatar
cp src/di-auth/default.jpg ~/data/di-data/di-auth/avatars/ || { echo "Failed to copy the default avatar."; exit 1; }

# Run the Docker Compose command
docker-compose up -d