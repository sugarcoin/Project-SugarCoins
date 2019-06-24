FROM ubuntu:latest

RUN apt-get -y update && apt-get -y upgrade

RUN apt-get -y install python3-pip

COPY requirements.txt /sugarcoins/
WORKDIR /sugarcoins

RUN pip3 install -r requirements.txt
