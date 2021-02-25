FROM python:3.9
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /code
WORKDIR /code

COPY requirements/development.txt requirements/base.txt /code/requirements/
RUN pip install -r requirements/development.txt

COPY compose/dev/django/start.sh /

COPY . /code/