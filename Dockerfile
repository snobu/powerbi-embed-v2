FROM ubuntu:latest
MAINTAINER Adrian Calinescu "adcaline@microsoft.com"
RUN apt-get update -y \
    && apt-get install -y python3 \
    python3-dev \
    python3-pip


RUN mkdir /app

COPY * /app/
WORKDIR /app

RUN pip3 install -r requirements.txt

RUN chmod 700 ./app.py

CMD python3 ./app.py

EXPOSE 5555