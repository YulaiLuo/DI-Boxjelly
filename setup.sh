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
mkdir -p ~/data/nginx/conf
mkdir -p ~/data/nginx/html
mkdir -p ~/data/nginx/ssl
mkdir -p ~/data/nginx/logs

# Copy nginx configuration file in the di-web directory to the desired location
cp -r nginx.conf ~/data/nginx/conf/ || { echo "Failed to copy files from the di-web directory."; exit 1; }

# Copy all files in the build directory to the desired location
cp -r build/* ~/data/nginx/html/ || { echo "Failed to copy files from the build directory."; exit 1; }

# Navigate back to the root directory
cd ../..

# Copy the default avatar
cp /src/di-auth/default.jpg ~/data/di-data/di-auth/avatars/ || { echo "Failed to copy the default avatar."; exit 1; }

# Run the Docker Compose command
docker-compose up -d