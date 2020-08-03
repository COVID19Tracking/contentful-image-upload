FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
RUN apk --update add bash nano
COPY ./requirements.txt /var/www/requirements.txt
RUN apt-get update && \
    apt-get install -y zlib1g-dev
RUN python -m pip install -U --force-reinstall pip
RUN pip install -r /var/www/requirements.txt
