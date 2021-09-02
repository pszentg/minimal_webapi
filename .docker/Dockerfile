FROM python:3.8.0
RUN apg-get update && apt-get upgrade && apt-get install -y redis-server
ADD . /python-flask
WORKDIR /python-flask
RUN pip install -r requirements.txt
EXPOSE 5000
