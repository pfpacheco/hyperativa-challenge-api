FROM python:3.9.19-slim-bullseye

RUN mkdir -p /opt/hyperativa

WORKDIR /opt/hyperativa

COPY . .

RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000