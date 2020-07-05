FROM django:server
WORKDIR /opt
COPY ./ILMS_Backend .
COPY ./nginx/nginx.conf .
COPY ./nginx/server.conf .
COPY ./nginx/logs .
COPY ./uwsgi/uwsgi.ini .
COPY ./requirements.txt .
RUN set -x \
    && pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple \
    && uwsgi --ini /opt/uwsgi.ini \
    && /usr/local/nginx/sbin/nginx -c /opt/nginx.conf
