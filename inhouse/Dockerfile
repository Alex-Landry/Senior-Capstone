FROM python:3.8.9-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUNBUFFERED 1

RUN apk update
RUN apk update && apk add gcc libc-dev make git libffi-dev openssl-dev python3 libxml2-dev libxslt-dev
RUN apk add postgresql-dev gcc python3-dev musl-dev libc-dev linux-headers 

RUN pip install --upgrade pip
COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .


#RUN chmod +x *

#RUN chmod -R 755 ./

#ENTRYPOINT ["./entrypoint.sh"]