# base image
FROM python:3

#maintainer
LABEL Author="CodeGenes"

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONBUFFERED 1

#directory to store app source code
RUN mkdir /pwitter

#switch to /app directory so that everything runs from here
WORKDIR /pwitter

#copy the app code to image working directory
COPY ./pwitter /pwitter

RUN apt-get update && apt-get install -y --no-install-recommends libmagic1 && rm -rf /var/lib/apt/lists/*

RUN pip install filemagic
#let pip install required packages
RUN pip install -r requirements.txt