---
layout: post
comments: true
title:  "Redmine, Jira 같이 사용하기"
date:   2018-01-16 18:00:00 +0900
categories: back-end
description: Jira, redmine 동기화 개발을 위한 개발환경 구축
---
# Redmine, Jira 같이 사용하기

[Redmine docker](https://hub.docker.com/_/redmine/), [Jira docker](https://hub.docker.com/r/cptactionhank/atlassian-jira/) 설치

```bash
# docker redmine official image 다운로드
docker pull redmine

# redmine 서버 포트 3000
docker run --privileged -d -p 3000:3000 --name remine_server redmine

# 서버 동작 확인
docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
bdb6e6b2a512        redmine             "/docker-entrypoint.…"   7 minutes ago       Up 7 minutes        0.0.0.0:3000->3000/tcp   redmine_server

# docker jira image 다운로드
docker pull cptactionhank/atlassian-jira

# jira 서버 포트 8080
docker run -d -p 8080:8080 --name jira_server f0c298620dd2
```

[Jira API를 이용한 매쉬업 서비스 개발](https://www.joinc.co.kr/w/man/12/jira)을 참고 하여 개발 진행

## Jira REST API 사용하기

참고: [JIRA Server platform REST API reference](https://docs.atlassian.com/software/jira/docs/api/REST/7.6.1/?_ga=2.78912028.987396854.1516072212-399143127.1516072212)

#### 기본 구조

``` http
http://host:port/context/rest/api-name/api-version/resource-name
```
#### 예시 자기 정보 가져오기

- Basic Auth 필수

```http
GET /rest/api/2/myself
```

#### Response 결과

```json
{
  self:"http://localhost:8080/rest/api/2/user?username=id",
  key: "id",
  name: "name",
  emailAddress: "id@email.com",
  avatarUrls:{
    ...
  },
  displayName: "id@email.com",
    
  
}
```

## Redmine REST API 사용하기

참고: [Redmine API](http://www.redmine.org/projects/redmine/wiki/Rest_api)

### Request 방법

```http
GET /issue.[format]
```

```http
POST /issue.[format]
```

```http
PUT /issues/[id].[format]
```

```http
DELETE /issues/[id].[format]
```

#### Parameters

```
project_id
tracker_id
status_id
priority_id
subject
description
category_id
...
```

## 예제

### Request 요청

```javascript
Basic Auth
username: id
password: password
```

```http
POST /issues.json
```

```Json
{
    "issue": {
      "project_id": 1,
      "subject": "제목을 입력",
      "priority_id": 1,
      "description":"여기에 설명내용을 입력 "
    }
}
```

### Response 결과

```json
{
    "issue": {
        "id": 3,
        "project": {
            "id": 1,
            "name": "JIRA와 Redmine 동기화 개발"
        },
        "tracker": {
            "id": 1,
            "name": "신규"
        },
        "status": {
            "id": 1,
            "name": "신규"
        },
        "priority": {
            "id": 1,
            "name": "낮음"
        },
        "author": {
            "id": 1,
            "name": "mcauto"
        },
        "subject": "제목을 입력",
        "description": "설명 내용 ",
        "start_date": "2018-01-16",
        "done_ratio": 0,
        "spent_hours": 0,
        "total_spent_hours": 0,
        "created_on": "2018-01-16T07:19:47Z",
        "updated_on": "2018-01-16T07:19:47Z"
    }
}
```

위의 REST API를 호출하는 프로그램을 작성하여 동시에 글을 올릴 수 있다
