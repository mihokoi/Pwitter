# pull official base image
FROM python:3.10

# set work directory
WORKDIR /

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# install psycopg2
RUN apt-get update \
&& apt-get -y install g++ libpq-dev gcc unixodbc unixodbc-dev && apt-get install -y apt-utils

# install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# collect static files
RUN python manage.py collectstatic --noinput

# add and run as non-root user
RUN adduser --system --group pwitter
USER pwitter

# run gunicorn
CMD gunicorn django_social.wsgi:application --bind 0.0.0.0:$PORT
