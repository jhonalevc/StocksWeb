FROM tiangolo/uwsgi-nginx:python3.9

ENV UWSGI_CHEAPER 4
ENV UWSGI_PROCESSES 64
ENV NGINX_WORKER_PROCESSES auto
ENV NGINX_WORKER_CONNECTIONS 2048
ENV NGINX_WORKER_OPEN_FILES 2048


ENV LISTEN_PORT 8080

EXPOSE 8080

ENV STATIC_URL /static

ENV STATIC_PATH /var/www/app/static


COPY ./requirements.txt /var/www/requirements.txt

RUN pip install -r /var/www/requirements.txt

COPY . . /var/www/app/


CMD ["python", "/var/www/app/stocksweb.py"]
