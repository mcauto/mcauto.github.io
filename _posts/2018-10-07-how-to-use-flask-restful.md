---
layout: post
comments: true
title: "Python으로 API 개발하기"
date: 2018-10-07 18:00:00 +0900
categories: back-end
description: Python framework Flask-RESTful을 이용한 API개발
---

# Python으로 API 개발하기 1

### 개요

본 포스팅에서는 Python의 경량 프레임워크인 Flask를 이용하여 API를 개발하는 방법에 대하여 포스팅 할 예정이다.

Python의 Web Framework는 Django와 Flask가 있다.

Django는 강력한 모듈들이 기본으로 탑재되어있어 프레임워크와 파이썬 언어에 대한 이해도가 높을 경우 개발이 수월하지만 처음 개발하는 사람의 경우 프레임워크의 학습에 시간이 많이 소요될 수 있다.

하지만, Flask는 Web Application 개발에 필요한 뼈대만 존재하며 필요할 경우 module을 직접 개발하거나 설치하여 사용이 가능하다.

Django는 어느정도 완성도 높은 프레임워크에서 개발할 수 있는 장점이 있는 반면에 사용하지 않는 모듈들을 같이 포함하고 있어 다소 무겁고 어느정도 러닝커브가 존재한다.

Flask는 어플리케이션 개발에 필요한 모듈만을 사용하기 때문에 최적화된 프레임워크를 구축할 수 있다는 장점이 있는 반면에 모듈을 하나하나 구현해야하므로 모듈학습에 대한 러닝커브가 존재한다.

일반적으로 Python을 이용한 API개발은 Django REST Framework와 Flask RESTful을 이용한다.

그 중 본 글에서는 Flask RESTful을 이용한 API 개발 방법에 대해서 작성하려고한다.

### 개발환경

- Python3
- pipenv: 가상환경 구축 모듈(pip)
- vscode: 에디터
- postman: API Request tool
- Docker (+docker-compose)
  - Mysql container
- Python module
  - [pytest](https://docs.pytest.org/en/latest/): Python Test module
  - [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/): RESTful API 개발용
  - [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/latest/): SQLAlchemy의 Flask 버전 모듈
    - [SQLAlchemy](https://www.sqlalchemy.org/): Python SQL Toolkit, Object Relational Mapper(ORM)
- 추가 응용 모듈 (추후 업로드)
  - [Flask-RESTPlus](https://flask-restplus.readthedocs.io/en/stable/): Flask-RESTful + Swagger UI(Excutable, Visualizing APIs)
  - [marshmallow](https://marshmallow.readthedocs.io/en/latest/): simplified object serialization
  - [Marshmallow-jsonapi](https://marshmallow-jsonapi.readthedocs.io/en/latest/): serialization for json api
  - [Flask-migrate](https://flask-migrate.readthedocs.io/en/latest/): Python ORM migrate at Database

# How to?

#### 개발 순서

1. pipenv를 이용한 가상환경 구축 및 모듈 설치
2. docker를 이용한 database 실행
3. Flask app 구조 설계(폴더 구성하기)
4. API 개발하기
5. API 테스트하기

### 1. pipenv를 이용한 가상환경 구축 및 설치

기존 python을 개발할 때 pip을 이용하여 module을 설치한다.

전역으로 설치해서 사용해도 상관없지만 python은 version 2와 3의 차이로 인한 module의 문제가 발생하므로 virtualenv를 이용한 가상개발환경를 구성하여 가상환경에 module을 설치하는 것을 권장한다.

익숙해지면 상관없지만 처음 python을 학습하는 사람 입장에서는 생각보다 어렵고 번거로울 수 있다.

#### 기존 python 개발 flow [python3 개발환경 구축](https://mcauto.github.io/back-end/2018/01/13/python-django-gunicorn/)

```bash
# pip 설치
$ yum install python36u-pip python36u-devel
# virtualenv 사용
$ python3.6 -m venv {가상환경이름}
# 가상환경 활성화
$ source {가상환경이름}/bin/activate
# 모듈 한번에 설치(requirements.txt에 dependency를 입력해두고 설치)
$ pip install -r requirements.txt
# 모듈 단일 설치
$ pip install {모듈이름} # 설치 후에는 virtualenv의 lib 또는 lib64에 설치된다
# 개발 작업 ....
# ...
# 이후 작업 후
$ deactivate # 가상환경 빠져나오기
```

위와 같이 설치하는 단계가 많다. (번거로움)

이런 번거로움을 해결하기 위해서 나온것이 pipenv이다.

pipenv는 Python.org에서 공식적으로 권장하는 패키지 설치 툴이다.

pipenv는 이름에서 알수 있듯 pip과 virtualenv를 합친 module이다.

- Pip + virtualenv
- Requirements.txt > Pipfile
- .env를 이용한 workflow

#### pipenv 설치 및 사용 방법

```bash
$ pip install pipenv
$ pipenv install # 자동으로 pipfile을 인식하여 module 설치 진행
$ pipenv shell # 가상환경 진입
$ pipenv graph # 현재 설치된 모듈의 의존성 모듈들을 같이 보여줌
```

**Pipfile**

```pipfile
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
flask = "*"
flask-restful = "*"
pytest = "*"
pytest-cov = "*"
enum34 = "*"
[dev-packages]

[requires]
python_version = "3.6"
```

위와 같이 pipfile을 작성하고 

```bash
$ pipenv install
```

명령어를 실행하면 자동으로 packages에 있는 module들과 requires의 버전에 맞추어 module을 가상환경에 설치한다

이후 개발은 pipenv shell을 통하여 가상환경에 진입한 후 개발을 진행하면 된다.

#### 2. Docker를 이용한 MySQL 띄우기 (with docker-compose)

Docker는 Container 기술을 이용한 VM(?) 정도로 설명할 수 있을 것 같다. 자세한 설명은 다른 포스팅으로 작성예정

##### docker-compose.yml

```yaml
version: '2'
services:
  mysql:
    image: mysql:5.7
    hostname: mysql
    container_name: mysql
    command: --default-authentication-plugin=mysql_native_password
    restart: always
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_USER: user
      MYSQL_PASSWORD: password
      MYSQL_DATABASE: database
```

Docker와 Docker-compose를 설치하고 위와 같이 yml 파일을 작성한 뒤

```bash
$ docker-compose up
```

을 실행하면 mysql의 docker 이미지가 자동으로 다운로드되고 container로 띄워진다.