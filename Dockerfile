# Use an official Python runtime as a parent image
FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app/backend
WORKDIR /app/backend

COPY . /app/backend

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000
