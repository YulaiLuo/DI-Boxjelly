# Use the official Node.js image as the base image
FROM node:18-alpine

# Create the working directory
WORKDIR /src/di-web

# Copy the application source code to the working directory
COPY . .

# Copy package.json and yarn.lock files to the working directory
# COPY package.json yarn.lock ./

# Install project dependencies
RUN yarn install

# Build the production version of the application
RUN yarn build

# Install and configure 'serve' for hosting the React application in a production environment
RUN yarn global add serve

# Expose the port; this should match the port used in the serve command
EXPOSE 8002

# Start the application
CMD ["serve", "-s", "build", "-l", "8002"]

# Build image:
# sudo docker image build -t di_web .

# Run the container:
# sudo docker run -d --name di_web --network di -p 0.0.0.0:8000:8000 di_web:latest 
