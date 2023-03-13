# syntax=docker/dockerfile:1

# 设置基础镜像
FROM python:3.8-slim-buster

# 设置working directory
WORKDIR /webapp

# 复制requirement到镜像中
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# 复制所有的文件到镜像
COPY . .

CMD ["python3" , "app.py"]
# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port="]

# Build image:
# sudo docker image build -t corsa_web .

# Run the container:
# sudo docker run -d --name corsa_web -p 0.0.0.0:80:80 corsa_web:latest
