---
layout: post
comments: true
title: "Gitlab docker container로 설치하기"
date: 2018-10-14 22:04:00 +0900
categories: infra
description: Gitlab docker container 설치하기
---

# Gitlab docker container로 설치하기

## 개요

#### Gitlab이란?

버전 관리 시스템인 Git과 이슈관리, CI/CD 등 프로젝트와 관련된 다양한 기능들을 사용할 수 있으며, 자신의 서버에 직접 설치해서 사용할 수 있다.

#### Docker란?

Docker는 Linux 기반의 Container RunTime [오픈소스](https://github.com/docker)

## 설치

1. docker,  docker-compose설치
```bash
$ yum install docker, docker-compose
```
2. docker-compose.yml 작성


```yaml
version: '3'
services:
  gitlab:
    image: 'gitlab/gitlab-ce:latest'
    restart: always
    container_name: gitlab
    ports:
      - '80:80'
      - '443:443'
      - '22:22'
    volumes:
      - './gitlab/config:/etc/gitlab'
      - './gitlab/logs:/var/log/gitlab'
      - './gitlab/data:/var/opt/gitlab'
```
3. container 실행

```bash
$ docker-compose up -d
```


4. localhost 접속(http:://localhost.com)
5. Root계정 등록

![gitlab-root-registration](/assets/img/how-to-install-gitlab/gitlab-root-registration.png)

6. Gitlab 사용하기

![gitlab-main](/assets/img/how-to-install-gitlab/gitlab-main.png)



