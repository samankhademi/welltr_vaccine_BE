FROM python:3
LABEL MAITAINER="SINA EBRAHIMNEZHAD <eb.sina@gmail.com>"

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y gettext

RUN pip3 install --upgrade setuptools
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN python3 manage.py compilemessages
