---
layout: post
comments: true
title: "MacOS에 python3 설치하기(+ pipenv)"
date: 2018-10-18 22:33:00 +0900
categories: infra
description: Mac에 python3 설치하기
---

1) Install Python 3.6.x from <https://www.python.org/downloads/> or [homebrew](http://brew.sh/). 

```
$ brew install python3   # Installed at /usr/local/{user}/python3
```
python 버전 확인
```
$ python3
>>> Python 3.6.5
```
2) pip 설치하기 (brew로 설치했을 경우는 패스)

```sh
$ curl -O https://bootstrap.pypa.io/get-pip.py
$ sudo python3 get-pip.py
```
3) pipenv 설치하기

```bash
$ pip3 install pipenv
```

