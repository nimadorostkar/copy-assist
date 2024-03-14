FROM python:3.10-slim-buster

WORKDIR /copy_assist

COPY /requirements/requirements.txt /copy_assist/requirements/

RUN pip install --upgrade pip

RUN apt-get update && apt-get upgrade -y

RUN pip install -r requirements/requirements.txt

COPY . /copy_assist


EXPOSE 8000 9000