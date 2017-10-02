FROM python:2.7

RUN apt-get update -y
RUN apt-get install -y rsync

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN pip install tox