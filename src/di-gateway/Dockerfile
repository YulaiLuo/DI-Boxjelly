# set up the base python image
FROM python:3.9.16-slim-bullseye

# set the working directory
WORKDIR /src/di-gateway

# install gcc and python3-dev
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# upgrade pip
RUN /usr/local/bin/python -m pip install --upgrade pip

# duplicate the required library into the base image
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# copy all file into the image
COPY . .

EXPOSE 8000

# start the program
CMD ["gunicorn" , "main:app", "-c", "gunicorn_config.py"]

# Build image:
# sudo docker image build -t di-gateway .

# Run the container:
# sudo docker run -d --name di-gateway --network di di-gateway:latest
