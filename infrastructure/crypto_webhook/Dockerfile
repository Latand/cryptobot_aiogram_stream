FROM python:3.11-slim

WORKDIR /usr/src/app/api

COPY ./infrastructure/crypto_webhook/requirements.txt /usr/src/app/api/requirements.txt
RUN pip install -r /usr/src/app/api/requirements.txt

COPY . /usr/src/app/api