---
layout: post
comments: true
title: "Python으로 API 개발하기"
date: 2018-10-11 23:13:00 +0900
categories: back-end
description: Python framework Flask-RESTful을 이용한 API개발
---

# Python으로 API 개발하기

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
  - [Flask-migrate](https://flask-migrate.readthedocs.io/en/latest/): Python ORM migrate at Database (such as Django migrate)
  - [marshmallow](https://marshmallow.readthedocs.io/en/latest/): simplified object serialization
    - [Marshmallow-jsonapi](https://marshmallow-jsonapi.readthedocs.io/en/latest/): serialization for json api
- 추가 응용 모듈 (추후 업로드)
  - [Flask-RESTPlus](https://flask-restplus.readthedocs.io/en/stable/): Flask-RESTful + Swagger UI(Excutable, Visualizing APIs)



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
pytest = "*"
pytest-cov="*"
flask-restful = "*"
flask-sqlalchemy = "*"
flask-migrate = "*"
flask-script = "*"
enum34="*"
pymysql = "*"
python-dotenv = "*"
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



#### 3. Flask App 구조 설계


```bash
Flask-RESTful-example
├── .flaskenv
├── Pipfile 
├── README.md
├── app
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   └── database.py # SQLAlchemy
│   ├── books # API Namespace example 
│   │   ├── __init__.py
│   │   ├── models.py # SQLAlchemy ORM Model, marshmallow Schema
│   │   └── views.py # Flask Resource (such as Controller)
│   ├── config.py # app config
│   └── log # log folder
├── docker-compose.yml
├── images
└── run.py
```

app: Flask application

app/api: RESTful API 공통 명세 영역. 각 namespace의 view에 작성된 api의 route를 등록

app/api/database.py: SQLAlchemy 인스턴스와 SQL에서 공통으로 사용되는 Create, Update, Delete 정의

app/books: book model의 namespace

app/books/models.py: SQLAlchemy ORM과 marshmallow의 Schema 사용하여 데이터베이스 모델 설계

app/books/views.py: Flask-RESTful의 Resource를 이용하여 API 구현 (일반적으로 Item과 List를 구현)

app/config.py: app의 설정

app/log: app의 로그 저장위치

docker-compose.yml: application 실행에 필요한 컨테이너 명세(mysql)

images: README.md에 사용되는 이미지 리소스

run.py: flask app의 main 실행 진입점

#### 4.API 개발하기

위에서 설계한 구조에서 API를 개발하기 위해서는 다음과 같은 4단계로 이루어지며

1번은 설정이므로 처음에만 작성하고 추후 2~4번 항목들을 반복해서 개발한다.

1. SQLAlchemy를 이용하여 데이터베이스와 연결
2. model 클래스 설계
3. Resource 설계 (다른 프레임워크에서는 흔히 Controller)
4. URL routing

**app.api.database.py (SQLAlchemy 인스턴스 생성, 공통 함수 구현)**

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CRUD:   
    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()   

    def update(self):
        return db.session.commit()

    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()
```

**app.config.py (database 연결을 위한 설정)**

```python
"""
Global Flask Application Setting

set FLASK_CONFIG to 'development
 """

import os

class Config:
    # If not set fall back to production for safety
    FLASK_ENV =  os.getenv('FLASK_ENV', 'production')
    # Set FLASK_SECRET on your production Environment
    SECRET_KEY = os.getenv('FLASK_SECRET', 'Secret')

    APP_DIR = os.path.dirname(__file__)
    ROOT_DIR = os.path.dirname(APP_DIR)

    HOST = '0.0.0.0'
    PORT = '5000'
    DEBUG = True

    LOG_PATH = os.path.abspath(APP_DIR)+"/log"

    MYSQL_DATABASE_USERNAME='user'
    MYSQL_DATABASE_PASSWORD='userpassword'
    MYSQL_DATABASE_NAME='database'
    MYSQL_DATABASE_HOST='localhost'
    MYSQL_PORT=os.getenv('MYSQL_PORT','33306')

    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_ADDR}:{DB_PORT}/{DB_NAME}?charset=utf8"
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.format(DB_USER=MYSQL_DATABASE_USERNAME,
                                                             DB_PASS=MYSQL_DATABASE_PASSWORD,
                                                             DB_ADDR=MYSQL_DATABASE_HOST,
                                                             DB_PORT=MYSQL_PORT,
                                                             DB_NAME=MYSQL_DATABASE_NAME)

```



**app.books.models.py (model 클래스 설계)**

```python
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from marshmallow_jsonapi.flask import Schema
from marshmallow_jsonapi import fields
from marshmallow import validate

from app.api.database import db
from app.api.database import CRUD

class Books(db.Model, CRUD):
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    creation_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    is_rent = db.Column(db.Boolean, default=True, nullable=False)
    
    def __init__(self, name, is_rent):
        self.name = name
        self.is_rent = is_rent

class BooksSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')
    id = fields.Integer(dump_only=True)
    name = fields.String(validate=not_blank)
    is_rent = fields.Boolean()
    #self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/api/books"
        else:
            self_link = "/api/books/{}".format(data['id'])
        return {'self': self_link}

    class Meta:
        type_ = 'books'
```

**app.books.views.py ( Resource 구현 )**

```python
from flask import jsonify
from flask import make_response
from flask import Blueprint

from flask_restful import Resource
from flask_restful import Api
from flask_restful import reqparse
from flask_restful import abort
from flask_restful import fields
from flask_restful import marshal_with

from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from app.books.models import Books
from app.books.models import BooksSchema
from app.api.database import db

books_api = Blueprint('books', "Book's API")
schema = BooksSchema()
book_fields = {
    'id': fields.Integer,
	'name': fields.String,
    'is_rent': fields.Boolean
}
class BookItem(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('name', type=str, help="book's name",location='json')
	parser.add_argument('is_rent', type=int, help='is it rentable?',location='json')
	body = ''
	status_code = 501 # NOT_IMPLEMENTED
	def get(self, book_id):
		book_query = Books.query.get_or_404(book_id)
		book = schema.dump(book_query).data
		return book

	def patch(self, book_id):
		args = self.parser.parse_args()
		book = Books.query.get_or_404(book_id)
		for key, value in args.items():
			setattr(book, key, value)
		try:
			book.update()
			self.body = jsonify(schema.dump(book).data)
			self.status_code = 200 # OK
		except IntegrityError as error:
			db.session.rollback()
			error_message = str(error) 
			self.body = jsonify({"error": error_message, "type":"IntegrityError"})
			if "Duplicate entry" in error_message:
				self.status_code = 409 # CONFLICT
			else:
				self.status_code = 400 # BAD REQUEST
		finally:
			response = (self.body, self.status_code.value)
			response = make_response(response)

		return response

	def delete(self, book_id):
		return {'book_id': book_id, 'method':'delete'}

class BooksList(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('name', required=True, type=str, help="book's name",location='json')
	parser.add_argument('is_rent', type=int, help='is it rentable?',location='json')
	body = ''
	status_code = 501

	def get(self):
		books_query = Books.query.all()
		results = schema.dump(books_query, many=True).data
		self.body = jsonify(results)
		self.status_code = 200
		response = (self.body, self.status_code)
		return make_response(response)

	def post(self):
		args = self.parser.parse_args()
		book = Books(name=args['name'],
					is_rent=args['is_rent'])
		try:
			book.add(book) 
			query = Books.query.get(book.id)
			self.body = jsonify(schema.dump(query).data)
			self.status_code = 201

		except IntegrityError as error:
			db.session.rollback()
			import os
			error_message = str(error) 
			self.body = jsonify({"error": str(error), "type":"IntegrityError"})
			if "Duplicate entry" in error_message:
				self.status_code = 409
			else:
				self.status_code = 400
		finally:
			response = (self.body, self.status_code.value)
			response = make_response(response)

		return response

```

**app.api.py (Routing)**

```python
from app.books.views import books_api
from app.books.views import BookItem
from app.books.views import BooksList
from flask_restful import Api

api = Api(books_api)
api.add_resource(BookItem, '/<int:book_id>')
api.add_resource(BooksList, '/')

```

**app.py**

```python
import os
from flask import Flask, current_app, send_file
from app.api import books_api

from logging.config import dictConfig
from app.books.models import db
from app.config import Config
import logging

def create_app(config_filename):
    if 'TRAVIS_CI' not in os.environ:
        dictConfig({
            'version':1,
            'formatters': {
                'default': {
                    'format': '%(asctime)s] [%(levelname)s] [%(module)s:%(lineno)d]\n %(message)s',
                },
            },
            'handlers': {
                'file_handler': {
                    'class': 'logging.FileHandler',
                    'filename': Config.LOG_PATH + '/app.log',
                    'formatter': 'default',
                },
            },
            'root': {
                'level': 'INFO',
                'handlers': ['file_handler']
            }
        })
    
    app = Flask(__name__)
    app.config.from_object(config_filename)
    db.init_app(app)
    
    app.register_blueprint(books_api, url_prefix='/api/books')


    app.logger.info('>>> {}'.format(Config.FLASK_ENV))
    return app
```

**run.py**

```python
import os

from app import create_app

app = create_app('app.config.Config')

if __name__ == '__main__':
    app.run(host=app.config['HOST'],
            port=app.config['PORT'],
            debug=app.config['DEBUG'])
```



코드 실행 및 전체 소스코드는 [Flask-RESTful-example](https://github.com/mcauto/Flask-RESTful-example)에서 확인 가능

