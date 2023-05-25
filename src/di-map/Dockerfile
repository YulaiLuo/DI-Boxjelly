# syntax=docker/dockerfile:1

# set up the base python image
FROM python:3.9.16-slim-bullseye

# set the working directory
WORKDIR /src/di-map

# duplicate the required library into the base image
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

# copy all file into the image
COPY . .

EXPOSE 8003
# start the program
CMD ["gunicorn" , "main:app", "-c", "gunicorn_config.py"]

# Build image:
# sudo docker image build -t di-map .

# Run the container:
# sudo docker run -d --name di-map -v /home/ubuntu/etc/medcat_model:/src/di-map/app/controllers/medcat_model --network di di-map:latest
