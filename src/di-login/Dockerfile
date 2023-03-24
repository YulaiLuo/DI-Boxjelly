# syntax=docker/dockerfile:1

# set up the base python image
FROM python:3.8-slim-buster

# set the working directory
WORKDIR /src/backend

# duplicate the required library into the base image
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# copy all file into the image
COPY . .

# start the program
CMD ["python3" , "app.py"]
# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port="]

# Build image:
# sudo docker image build -t di_boxjelly_backend .

# Run the container:
# sudo docker run -d --name di_boxjelly_backend -p 0.0.0.0:80:80 di_boxjelly_backend:latest
