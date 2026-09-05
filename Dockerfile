FROM python:3.11-slim-bookworm

LABEL org.opencontainers.image.source=https://github.com/Slickerius/IrnusDL

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get update \
    && apt-get install --yes zip
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN pip install 'uvicorn[standard]'

COPY . .
RUN mkdir -p static/tmp
