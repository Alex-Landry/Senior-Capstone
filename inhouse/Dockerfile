FROM python:3.8.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUNBUFFERED 1

RUN mkdir /home/app
RUN mkdir /home/app/web
RUN mkdir /home/app/web/staticfiles
RUN mkdir /home/app/web/mediafiles
WORKDIR /home/app/web

RUN apk update && apk add gcc libc-dev make git libffi-dev openssl-dev python3 libxml2-dev libxslt-dev
RUN apk add postgresql-dev gcc python3-dev musl-dev libc-dev linux-headers
RUN apk add libpq

RUN pip install --upgrade pip
COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . /home/app/web
COPY ./scripts /scripts
RUN chmod +x /scripts/*


ENTRYPOINT ["/scripts/entrypoint.sh"]