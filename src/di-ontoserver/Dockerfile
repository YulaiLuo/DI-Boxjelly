# set up the base python image
FROM python:3.9.16-slim-bullseye

# set the working directory
WORKDIR /src/di-ontoserver

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# copy all file into the image
COPY . .

# Make port 80 available to the world outside this container
EXPOSE 8080

# Run upload_uil.py when the container launches
CMD ["python", "upload_uil.py"]
