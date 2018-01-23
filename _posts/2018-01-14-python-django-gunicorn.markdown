---
layout: post
comments: true
title:  "Python 개발 환경 구축과 배포를 한번에!"
date:   2018-01-14 00:21:13 +0900
categories: back-end
description: Python 개발 환경 구축
---

# **Python 개발 환경 구축**

​	사용 스택: Docker, Python3.6, Django, Nginx, Mysql, gunicorn

### **Docker**

​	~~배포의 고통을 줄이기~~  유지보수를 위해 개발서버는 도커로 구축

```bash
# centos 이미지 다운로드
docker pull centos:latest

# 컨테이너 생성
docker run --privileged -d -p 80:80 -p 3306:3306 -p 21:21 --name xms centos:latest /sbin/init 

# 생성된 컨테이너에 연결
docker exec -it xms bash
```

privileged: 컨테이너 안에서 호스트의 리눅스 커널 기능을 모두 사용

d, detach: Detached 모드, 데몬 모드로 백그라운드 유지

p, publish: 포트 열기 추가 마다 앞에 붙여줌

 -p <Host port>: <Container port>

name: 컨테이너 이름 정하기 <이름> <이미지>

/sbin/init 를 입력해주지 않으면 Centos에서 아래와 같은 에러 발생

```
Failed to get D-Bus connection: No connection to service manager
```

[Docker 명령어 더 알아보기](http://pyrasis.com/book/DockerForTheReallyImpatient/Chapter20/28)


### 1. centos 7에 nginx 설치

출처: [CentOS7 - nginx 설치하기](http://opencode.co.kr/linux_tips/554?&page=2) 

```Bash
vim /etc/yum.repos.d/nginx.repo
```

```Bash
[nginx] 
name=nginx repo 
baseurl=http://nginx.org/packages/mainline/centos/7/$basearch/ 
gpgcheck=0 
enabled=1 
```

```Bash
# nginx 설치 시작
yum install nginx

# 서비스 가동
systemctl start nginx
systemctl enable nginx

# nginx 설정파일 경로 /etc/nginx/conf.d
# nginx 사용자 디렉토리 /etc/share/nginx/html
```



### **2. centos 7 에 python3 설치**

출처: [How to install Python 3.6.1 on CentOS 7](https://janikarhunen.fi/how-to-install-python-3-6-1-on-centos-7.html)

#### 필수 유틸리티 설치

```bash
yum update
yum install yum-utils
yum groupinstall development
```

#### Python3.6 설치

```Bash
# Repository
yum install http://centos7.iuscommunity.org/ius-release.rpm

# 파이썬 설치
yum install python36u

# 버전 확인
python3.6 -V

# pip 설치
yum install python36u-pip
yum install python36u-devel

# Python 버전 확인
python -V
# 출력
Python 2.7.5

# Python3 버전 확인
python3.6 -V
Python 3.6.1
```

#### 파이썬 가상환경(virtual environment) 사용

- 파이썬 버전 별 프로젝트 작업 가능

```bash
# 가상환경 만들기
python3.6 -m venv venv

# 가상환경 사용
. venv/bin/activate 또는 source venv/bin/activate
```



#### Django - Nginx - gunicorn 연동하기

출처: [Django 배포하기](https://wikidocs.net/6601)

```Bash
# 프로젝트 경로 설정
cd /var/www/html
mkdir django_test
cd django_test

# 가상환경 사용
python3.6 -m venv venv
. venv/bin/activate

# Django, gunicorn 설치
pip install Django gunicorn

# gunicorn.sock 파일이 저장될 위치
mkdir run
django-admin.py startproject conf .
```

##### django 설정

```Bash
vim conf/setting.py
```

```Bash
.
.
.
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
```

```bash
./manage.py makemigrations
./manage.py migrate
./manage.py createsuperuser
./manage.py collectstatic
./manage.py runserver 0.0.0.0:80
```

브라우저에서 http://서버_아이피 접속 확인

##### Gunicorn

구동 테스트

```Bash
gunicorn --bind 0.0.0.0:80 conf.wsgi:application
```

브라우저에서 http://서버_아이피 접속 확인

```Bash
deactivate
```

django, gunicorn 설치 및 설정 완료!

```Bash
vim /etc/systemd/system/gunicorn.service
```

```Bash
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/var/www/html/django_test
ExecStart=/var/www/html/django_test/venv/bin/gunicorn \
        --workers 3 \
        --bind unix:/var/www/html/django_test/run/gunicorn.sock \
        conf.wsgi:application

[Install]
WantedBy=multi-user.target
```

```Bash
# gunicorn 구동
systemctl start gunicorn
systemctl enable gunicorn

# 상태 확인
systemctl status gunicorn
```

#### Nginx

```bash
vim /etc/nginx/conf.d/django_test.conf
```

```bash
server {
        listen 80;
        server_name 0.0.0.0;

        location = /favicon.ico { access_log off; log_not_found off; }

        location /static/ {
                root /var/www/html/django_test/static/;
        }

        location / {
                proxy_set_header Host $http_host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;

                proxy_pass http://unix:/var/www/html/django_test/run/gunicorn.sock;
        }
}
```

```bash
# nginx config 문법 검사 및 재기동
nginx -t
```



#### **CentOS 7 MySQL Install**

출처: [How to Install MySQL on CentOS 7](https://linode.com/docs/databases/mysql/how-to-install-mysql-on-centos-7/)

```bash
yum install wget
wget http://repo.mysql.com/mysql-community-release-el7-5.noarch.rpm
rpm -ivh mysql-community-release-el7-5.noarch.rpm
yum update
yum install mysql-server
systemctl start mysqld
```

**Django & mysql 연동 **
