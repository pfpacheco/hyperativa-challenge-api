FROM python:3.9.8

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/main

COPY ../../ .

RUN pip install --upgrade pip setuptools wheel easy_setup
RUN pip install --no-cache-dir -r ./requirements.txt

EXPOSE 8000