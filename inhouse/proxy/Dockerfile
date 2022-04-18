FROM nginx:1.21-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY default.conf /etc/nginx/conf.d


COPY ./default.conf /etc/nginx/conf.d/default.conf
COPY uwsgi_params /etc/nginx/uwsgi_params