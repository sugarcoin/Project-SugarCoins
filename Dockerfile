FROM jwilder/dockerize

COPY . /sugarcoins/
WORKDIR /sugarcoins

RUN apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev python3-dev

RUN pip3 install -r requirements.txt

ENTRYPOINT dockerize -wait tcp://db:5432 python3 server.py
