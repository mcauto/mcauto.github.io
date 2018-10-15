---
layout: post
comments: true
title: "pipenv install 'module' object is not callable 에러 해결방법"
date: 2018-10-15 21:00:00 +0900
categories: back-end
description: pipenv install 시 module object 에러
---

# 'module' object is not callable 에러

```bash
$ pipenv --three
$ pipenv install [library]
```

pipenv를 이용하여 처음 프로젝트를 시작할 때 아래와 같은 에러 메시지가 발생한다.

```bash
Pipfile.lock not found, creating...
Locking [dev-packages] dependencies...
Locking [packages] dependencies...
env/utils.py", line 402, in resolve_deps
    req_dir=req_dir
  File "/usr/local/lib/python3.7/site-packages/pipenv/utils.py", line 250, in actually_resolve_deps
    req = Requirement.from_line(dep)
  File "/usr/local/lib/python3.7/site-packages/pipenv/vendor/requirementslib/models/requirements.py", line 704, in from_line
    line, extras = _strip_extras(line)
TypeError: 'module' object is not callable
```

해당 버그 는 pipenv의 `18.1, 2018.7.1` 버전에서 발견된 버그이다.

```bash
$ pipenv run pip install pip==18.0
```

위와 같은 명령어로 pip 버전을 내리는 방법도 있으나 pipenv를 업그레이드 하는 방법으로 해결

```bash
$ brew upgrade pipenv
```

