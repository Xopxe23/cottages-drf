FROM python:latest

COPY requirements.txt /temp/requirements.txt

COPY . /cottages-app

WORKDIR /cottages-app

EXPOSE 8000

RUN pip install -r requirements.txt

RUN adduser --disabled-password cottages-user

USER cottages-user
