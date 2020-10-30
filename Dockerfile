FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install gcc
RUN apt-get update
RUN apt-get -y install gcc

# Upgrade pip
RUN python -m pip install --upgrade pip

# Requirements are installed here to ensure they will be cached.
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

RUN mkdir app
COPY . /app

WORKDIR /app

ENTRYPOINT ["scrapy", "runspider", "cfm_spider.py"]
