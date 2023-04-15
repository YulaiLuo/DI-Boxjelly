# syntax=docker/dockerfile:1

# set up the base python image
FROM python:3.9.16-slim-bullseye

# set the working directory
WORKDIR /src/di-auth

# duplicate the required library into the base image
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# copy all file into the image
COPY . .

EXPOSE 8001

# start the program
CMD ["gunicorn" , "main:app", "-c", "gunicorn_config.py"]

# Build image:
# sudo docker image build -t di_auth .

# Run the container:
# sudo docker run -d --name di_auth --network di -p 0.0.0.0:8001:8001 di_auth:latest 
