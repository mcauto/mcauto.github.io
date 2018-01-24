---
layout: post
comments: true
title:  "Redmine, Jira 같이 사용하기 3"
date:   2018-01-18 21:25:00 +0900
categories: back-end
description: Jira Webhook Post json 과 Redmine REST api 분석
---
# MyWebhook 개요

```
URL http://1c4fc821.ngrok.io/webhook
이벤트 이슈 관련 이벤트
      JQL: 모든 이슈
      이슈: 생성, 업데이트됨, 작업 로그 변경됨
      댓글: 생성, 업데이트됨, 삭제되었습니다.
      작업기록: 생성, 업데이트됨, 삭제되었습니다.
      이슈 연결: 생성, 삭제되었습니다.

      프로젝트 관련 이벤트
      프로젝트: 생성, 삭제되었습니다.
      버전: 생성, 삭제되었습니다.
본문 제외 아니요
전환 연결된 전환 없음.
```

위와 같이 웹훅을 설정하고 Jira의 이슈를 만들고 Webhook POST json을 확인

Redmine의 포스팅에 필요한 정보만을 간추림

# JIRA WEBHOOK Event JSON

### 프로젝트 생성, 수정, 삭제

```json
{
  webhookEvent:"project_created",
  project:{
    name:"Project make",
    key:"PM"
  },
  projectLead:{
    name:"mcauto"
  }
}
```

### 이슈 생성, 수정, 삭제

```json
{
  webhookEvent:"jira:issue_created",
  issue_event_type_name:"issue_created",
  user:{},
  issue:{
    id:"10015",
    key:"SJR-16",
    fields:{
      issuetype:{
        description:"해야 할 일",
        name: "작업"
      },
      project:{
        key:"SJR",
        name:"Sync JIRA, Redmine"
      },
      creator:{
        name:"mcauto",
        key:"mcauto",
        emailAddress:"mcauto@naver.com",
      },
      description: "make",
      summary:"make",
      priority:{
        name:"Medium",
        id:"3"
      }
    }
  }
}
```

```json
{
  webhookEvent:"jira:issue_updated",
  issue_event_type_name:"issue_created",
  changelog:{
    id:"10013",
    items:[
      {
        ...
      },
      {
        field:"status",
        fromString: "Done",
        toString:"To Do"
      }
    ]
  }
}
```

```json
{
  webhookEvent:"jira:issue_deleted",
  fields:{
    description:"content",
    summary:"title",
  }
}
```

### 댓글 등록, 수정, 삭제

댓글 관련 작업은 이슈도 수정되는 현상이므로 Event가 2번 발생

```json
{
  webhookEvent:"comment_created",
  comment:{
    author:{
      name:"mcauto"
    },
    body:"댓글 쓰기"
  }
}
```

```json
{
  webhookEvent:"jira:issue_updated",
  issue_event_type_name:"issue_commented",
  user:{
    name:"mcauto"
  },
  issue:{},
  // comment는 동일
  comment:{
    author:{
      name:"mcauto"
    },
    body:"댓글 쓰기"
  }
}
```

이와 같이 수정과 삭제 시 Event명은 다음과 같다 comment_updated, comment_deleted

위의 json을 이용하여 Redmine api 호출

# Redmine REST API 사용

REST API를 사용하기 위해서는 **관리 > 설정 > API > REST 웹서비스 활성화** 체크

## Authentication

- Basic Authentication
- API Key를 param에 담아서 보내기
- HTTP header에 "X-Redmine-API-Key"에 API key를 담아 보내기

Redmine API Key는 **사용자 정보 > 내계정 > API 접근키**에서 확인

## Project 생성

```http
POST /projects.json
```

#### Pramameter

```json
{
  "key":"required",
  "project":{
    "name":"required",
    "identifier":"required",
    "description":"",
    "homepage":"",
    "is_public":true of false,
    "parent_id":"parent project number",
    "inherit_members":true or false,
    "tracker_ids":"",
    "enabled_module_names:"",
  }
}
```

### 예시


```json
{
	"key":"발급받은 API 키",
	"project":{
		"name":"프로젝트명",
		"identifier":"PRO"
	}
}
```

## Issue 생성

참고: [python-redmine](https://python-redmine.com/resources/issue.html)

```http
POST /issues.[format]
```

### Parameter

```json
{
  "key":"required",
  "issue":{
    "project_id":"required",
    "tracker_id":"",
    "status_id":"",
    "priority_id":"required",
    "subject":"required",
    "description":"",
    "category_id":"",
    "fixed_version_id":"",
    "assigned_to_id":"",
    "custom_fields":"",
    "watcher_user_ids":"",
    "is_private":"",
    "estimated_hours":"",
  }
}
```

## Testing code by python

```python
from flask import Flask, request
import json, requests

app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        json_data = request.data.decode('utf-8')
        headers = {'content-type': 'application/json', 'X-Redmine-API-Key': '8d8625c456c6e996de3baaa53065e05204463e02'}
        j = {
            "issue": {
                "project_id": project_id,
                "subject": "Example",
                "priority_id": priority_id,
                "assigned_to_id": user_id
            }
        }
        r = requests.post('http://redmine_server:3000/issues.json', headers=headers, data=json.dumps(j))
        r = requests.post('http://1c4fc821.ngrok.io', headers=headers, data=json.dumps(j))

    return ''

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=80)
```

ngrok 확인결과 정상적으로 post결과 값이 온 것을 확인
