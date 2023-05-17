# syntax=docker/dockerfile:1

# set up the base python image
FROM python:3.9.16-slim-bullseye

# set the working directory
WORKDIR /src/di-center

# duplicate the required library into the base image
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# copy all file into the image
COPY . .

EXPOSE 8004
# start the program
CMD ["gunicorn" , "main:app", "-c", "gunicorn_config.py"]

# Build image:
# sudo docker image build -t di-center .

# Run the container:
# sudo docker run -d --name di-center --network di di-center:latest
