### Centos 中 (pymyslqclient错误)
yum -y install mysql-devel
### Ubuntu中 (pymyslqclient错误)
sudo apt install libmysqlclient-dev

### python 虚拟环境管理
yum -y install uwsgi
pip3 install virtualenv
virtualenv ilms_pyhton3 -p python3
source ilms_pyhton3/bin/activate


### Nginx 与 Nginx-upload-module 的安装
[参考文档](https://www.dazhuanlan.com/2020/01/04/5e10322451005/)
