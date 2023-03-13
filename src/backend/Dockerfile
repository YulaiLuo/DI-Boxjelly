# syntax=docker/dockerfile:1

# 设置基础镜像
FROM python:3.8-slim-buster

# 设置working directory
WORKDIR /src/backend

# 复制requirement到镜像中
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# 复制所有的文件到镜像
COPY . .

CMD ["python3" , "app.py"]
# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port="]

# Build image:
# sudo docker image build -t di_boxjelly_backend .

# Run the container:
# sudo docker run -d --name di_boxjelly_backend -p 0.0.0.0:80:80 di_boxjelly_backend:latest
