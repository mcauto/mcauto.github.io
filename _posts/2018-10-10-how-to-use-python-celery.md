---
layout: post
comments: true
title: "Python 분산처리 모듈 Celery 사용하기"
date: 2018-10-10 23:13:00 +0900
categories: back-end
description: Python 분산처리 모듈 Celery 사용하기
---

# Python 분산처리 모듈 Celery 사용하기

## 개요

Python에서 분산처리를 위한 모듈인 Celery를 이용하여 실시간 비동기 처리를 할 수 있다.
Celery를 이용하여 개발 전 간단하게 테스트해봤다.

## 시스템 구성

![project_structure](/assets/img/python-celery-project-structure/project_structure.png)

보라색 컴포넌트: 프로세스 매니지먼트

파랑색 컴포넌트: 애플리케이션

초록색 컴포넌트:  분산 메시지 처리 기반 비동기 작업

실제 시스템 구축시 위와 같이 3가지 컴포넌트들을 구현하여 데몬 서버를 돌릴 수 있다.

이 중 실제 분산처리에 해당하는 초록색 컴포넌트들을 구성하여 테스트를 진행하였다.

## 방법

##### docker-compose.yml

```yaml
version: '3'
services:
  redis:
    image: redis:latest
    command: ["redis-server", "--appendonly", "yes"]
    hostname: redis
    container_name: redis
    privileged: true
    sysctls:
      net.core.somaxconn: '511'
    volumes:
      - ./redis-data:/data
    ports:
      - 6379:6379
  rabbit:
    image: rabbitmq:3-management
    hostname: rabbitmq
    container_name: rabbitmq
    environment:
      RABBITMQ_ERLANG_COOKIE: 'SECRET_COOKIE_HERE'
      RABBITMQ_DEFAULT_USER: 'rabbitmq'
      RABBITMQ_DEFAULT_PASS: 'rabbitmq'
      RABBITMQ_DEFAULT_VHOST: '/'
    ports:
      - 15672:15672
      - 5672:5672
    volumes:
      - './rabbitmq:/var/lib/rabbitmq'
```

[RabbitMQ](https://hub.docker.com/_/rabbitmq/)와 [Redis](https://hub.docker.com/_/redis/)는 docker container를 사용하여 구성

##### Pipfile

```bash
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[dev-packages]

[packages]
celery="*"
circus="*"
flower="*"
chaussette="*"
eventlet="*"
dnspython="*"
scapy="*"
redis = "*"

[requires]
python_version = "3.6"
```

Python.org에서 공식적으로 권장하는 패키지인 [pipenv](https://medium.com/@erish/python-pipenv-%EB%9E%80-%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80-961b00d4f42f)를 이용하여 dependency 관리

##### portd.py

```python
from celery import Celery
from scapy.all import *
import time
BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

app = Celery('tasks',
             broker='pyamqp://rabbitmq:rabbitmq@localhost:5672//',
             backend=CELERY_RESULT_BACKEND)

app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.accept_content = ['json']
app.conf.result_expires = 3600

@app.task
def add(x,y):
    return x+y

s = conf.L3socket(iface='eth0')
@app.task
def ping_check(target, try_count=3, ports=default_ports):
    s.send(IP(dst=target)/ICMP())
    return "send ping"

if __name__ == '__main__':
    app.start()
```

테스트용 코드 작성

##### add_test.py

```python
from __init__ import add
from celery import group

result = group(add.s(i,i) for i in range(5))()
```

##### ping_test.py

```python
from __init__ import ping_check
from celery import group, chain
from random import randint

def random_ip():
    ip = [str(randint(0,255)) for _ in range(4)]
    ip = '.'.join(ip)
    return ip
dummy_list = set([random_ip() for _ in range(5000)])
result = group(ping_check.s(target=ip) for ip in dummy_list)()
print(len(result))
```