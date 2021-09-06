FROM python:3.8.0
RUN apt-get update && apt-get upgrade -y && apt-get install -y redis-server
ADD . /webapi
WORKDIR /webapi
RUN pip install -r requirements.txt
EXPOSE 5000
ENV PYTHONPATH "${PYTHONPATH}:/app/"