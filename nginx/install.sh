echo https://mirrors.ustc.edu.cn/alpine/latest-stable/main > /etc/apk/repositories
echo https://mirrors.ustc.edu.cn/alpine/latest-stable/community >> /etc/apk/repositories

apk update
apk add --no-cache --virtual .build-deps gcc libc-dev make openssl-dev pcre-dev zlib-dev linux-headers libxslt-dev gd-dev geoip-dev perl-dev libedit-dev mercurial alpine-sdk findutils wget bash

cd /opt
tar -zxvf nginx-1.16.1.tar.gz &&  tar -zxvf nginx-upload-module-2.3.0.tar.gz
cd nginx-1.16.1
./configure --add-module=../nginx-upload-module-2.3.0 --prefix=/usr/local/nginx --conf-path=/usr/local/nginx/conf/nginx.conf --pid-path=/usr/local/nginx/nginx.pid --with-http_ssl_module --with-http_gzip_static_module
make && make install
pip install uwsgi -i https://pypi.tuna.tsinghua.edu.cn/simple
