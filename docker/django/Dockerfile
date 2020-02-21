FROM python:3
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app
COPY app/requirements.txt /app/
RUN pip install -r requirements.txt

COPY ./app /app/

COPY ./docker/django/wait-for-it.sh /wait-for-it.sh

COPY ./docker/django/.bashrc /.bashrc
RUN apt-get update \
    && apt-get install -y dos2unix \
    && cat /.bashrc >> ~/.bashrc \
    && dos2unix ~/.bashrc \
    && rm /.bashrc
