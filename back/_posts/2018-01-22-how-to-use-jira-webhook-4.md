---
layout: post
comments: true
title:  "Redmine, Jira 같이 사용하기 5(완성)"
date:   2018-01-22 20:31:00 +0900
categories: back-end
---
# Jira Webhook Adapter 만들기 (to Redmine)

### Builder.py

```Python
from operator import eq
import json,requests


class Builder:
	def __init__(self, event):
		self.event = event

	def build(self):  # request에 필요한 json을 만들어냄
		result = {'rson': 'raise NotImplementedError()', 'type':'Exception'}
		return result

# CUD의 구조를 정하고 build에서 사용
class ProjectBuilder(Builder):
	def build(self):
		json = {
			'type': 'project builder'
		}
		self.crud = {
			'project_created': self.create,
			'project_updated': self.update,
			'project_deleted': self.delete
		}
		func = self.crud[self.event.webhookEvent]
		result = json if func == None else func()
		return result

	def create(self):
		e = self.event
		create_json = {
			'rson':{
				'project': {
					'name': e.proj_name,
					'identifier': e.proj_key,
					'description': '',
                    'custom_fields':[
						{
							'name':'jira::project_id',
							'value':e.proj_id, 
							'id':3
						}
					]
				},
				'type':'POST'
			}
		}
		return create_json

	def update(self):
		e = self.event
		update_json = {
			'rson':{
				'project': {
					'name': e.proj_name,
					'identifier': e.proj_key,
					'description': '',
					'custom_fields':[
						{
							'name':'jira::project_id',
							'value':e.proj_id, 
							'id':3
						}
					]
				},
				'type':'PUT'
			}
		}
		return update_json

	def delete(self):
		e = self.event
		delete_json = {
			'rson':{
				'project': {
					'identifier': e.proj_key,
					'description': '',
					'custom_fields':[
						{
							'name':'jira::project_id',
							'value':e.proj_id, 
							'id':3
						}
					]
				},
				'type':'DELETE'
			}
		}
		return delete_json

class IssueBuilder(Builder):
	def build(self):
		json = {
			'type': 'issue builder'
		}
		self.crud = {
			'jira:issue_created': self.create,
			'jira:issue_updated': self.update,
			'jira:issue_deleted': self.delete
		}
		func = self.crud[self.event.webhookEvent]
		result = json if func == None else func()
		return result

	def create(self):
		e = self.event
		create_json = {
			'rson':{
				'issue':{
					'id':e.issue_id,
					'project_id':e.issue_proj_key,
					'priority_id':e.issue_priority,
					'status_id':1,
					'subject':e.issue_summary,
					'description':e.issue_description,
					'assigned_to_id':1,
                    'custom_fields':[
						{
							'name':'jira::issue_id',
							'value':e.issue_id, 
							'id':4
						}
					]
				},
				'type':'POST'
			}
		}
		return create_json

	def update(self):
		e = self.event
		status = 2
		print(e.changelog.get('items'))
		if e.changelog.get('items') is not None :
			item = e.changelog.get('items').pop()
			status = int(item.get('to'))  
			if status == 10002:
				status = 3
			elif status == 10001:
				status = 5
			else:
				status = 2
		e.issue_priority = 6 - int(e.issue_priority)	
		update_json = {
			'rson':{
				'issue':{
					'id':e.issue_id,
					'project_id':e.issue_proj_key,
					'priority_id':(e.issue_priority),
					'status_id':status,
					'subject':e.issue_summary,
					'description':e.issue_description,
					'assigned_to_id':1,
					'custom_fields':[
						{
							'name':'jira::issue_id',
							'value':e.issue_id, 
							'id':4
						}
					]
				},
				'type':'PUT'
			}
		}
		return update_json

	def delete(self):
		e = self.event
		delete_json = {
			'rson':{
				'issue':{
					'id':e.issue_id,
					'custom_fields':[
						{
							'name':'jira::issue_id',
							'value':e.issue_id, 
							'id':4
						}
					]
				},
				'type':'DELETE'
			}
		}
		return delete_json 


class CommentBuilder(Builder):
	def build(self):
		json = {
			'type': 'comment builder'
		}
		self.crud = {
			'comment_created': self.create,
			'comment_updated': self.update,
			'comment_deleted': self.delete
		}
		func = self.crud[self.event.webhookEvent]
		result = json if func == None else func()
		return result

	def create(self):
		create_json = {
			'rson':{
				'issue':{
					'project_id':'',
					'priority_id':'',
					'status_id':'',
					'subject':'',
					'description':'',
					'assigned_to_id':'',
				},
				'type':'POST'
			}
		}
		return 'comment create'

	def update(self):
		update_json = {
			'rson':{
				'issue':{
					'project_id':'',
					'priority_id':'',
					'status_id':'',
					'subject':'',
					'description':'',
					'assigned_to_id':'',
				},
				'type':'PUT'
			}
		}
		return 'comment update'

	def delete(self):
		delete_json = {
			'rson':{
				'issue':{
					'project_id':'',
					'priority_id':'',
					'status_id':'',
					'subject':'',
					'description':'',
					'assigned_to_id':'',
				},
				'type':'DELETE'
			}
		}
		return 'comment delete'
```

### WebhookEvent.py

```Python
from Builder import *


class WebhookEvent:
  def __init__(self, dict):
    self.webhookEvent = dict.get('webhookEvent', None)
    self.issue_event_type_name = dict.get('issue_event_type_name', None)
    self.changelog = dict.get('changelog')
    self.isProject = 'project' in dict
    self.isComment = 'comment' in dict and self.issue_event_type_name == None
    if self.issue_event_type_name != None:
      self.isIssue = ('issue' in dict) and ('comment' not in dict) and self.issue_event_type_name.find('comment')
    else:
      self.isIssue = ('issue' in dict) and ('comment' not in dict)

    if self.isProject:
      self.proj = dict.get('project',None)
      self.proj_id = self.proj.get('id')
      self.proj_key = self.proj.get('key',None).lower()
      self.proj_name = self.proj.get('name',None)
      self.projectLead = self.proj.get('projectLead',None)
      self.author = '' if self.projectLead == None else self.projectLead.get('name')
    elif self.isComment:
      pass
    elif self.isIssue:
      self.issue = dict.get('issue',None)
      self.issue_id = int(self.issue.get('id',0))
      self.issue_key = self.issue.get('key',None).lower()
      self.issue_fields = self.issue.get('fields',None)
      self.issue_proj = self.issue_fields.get('project',None)
      self.issue_proj_id = int(self.issue_proj.get('id',0))
      self.issue_proj_key = self.issue_proj.get('key',None).lower()
      self.issue_summary = self.issue_fields.get('summary',None)
      self.issue_priority = self.issue_fields.get('priority',None).get('id')
      self.issue_description = self.issue_fields.get('description',None)
      
    else:
      pass
    self.builder = self.build()

  def build(self):
    if self.isProject:
      return ProjectBuilder(self)
    elif self.isComment:
      return CommentBuilder(self)
    elif self.isIssue:
      return IssueBuilder(self)
    else:
      return Builder(self)

  def toRson(self):
    return self.builder.build()
```

### webhook.py

```Python
from flask import Flask, request
import json, requests
from WebhookEvent import WebhookEvent

app = Flask(__name__)
base_url = 'http://redmine_server:3000'

@app.route('/',methods=['POST'])
def index():
    return ''

def is_json(myjson):
    try:
        json_object = json.dumps(myjson)
    except ValueError as e:
        return False
    return True

@app.route('/project',methods=['POST','DELETE'])
def project():
    req = init(request)
    rson = req.get('rson')
    headers = req.get('headers')

    if is_json(rson) and type(rson) is not str:
        rson = rson.get('rson',None)
        http_type = rson.get('type',None)
        data = {
            "project": rson.get('project')
        }
        if http_type == 'POST':
            r = requests.post(base_url+'/projects.json', headers=headers, json=data, timeout=3)
        elif http_type == 'DELETE':
            url = base_url+'/projects/'+str(rson.get('project').get('identifier'))+'.json'
            r = requests.delete(url, headers=headers, timeout=3)
        else:
            return 'Invalid Request'
    else:
        return 'Invalid Rson'

    return str(r.status_code)

@app.route('/issue',methods=['POST'])
def issue():
    req = init(request)
    rson = req.get('rson')
    headers = req.get('headers')
    
    if is_json(rson) and type(rson) is not str:
        rson = rson.get('rson',None)
        http_type = rson.get('type',None)
        data = {
            "issue": rson.get('issue')
        }
        if http_type == 'POST':
            r = requests.post(base_url+'/issues.json', headers=headers, json=data, timeout=3)
        elif http_type == 'PUT':
            id = get_issue_id(str(rson.get('issue').get('id')),headers)
            url = base_url+'/issues/'+id+'.json'
            r = requests.put(url, headers=headers, json=data, timeout=3)
        elif http_type == 'DELETE':
            id = get_issue_id(str(rson.get('issue').get('id')),headers)
            url = base_url+'/issues/'+id+'.json'
            r = requests.delete(url, headers=headers, timeout=3)
        else:
            return 'Invalid Request'
    else:
        return 'Invalid Rson'

    return str(r.status_code)

def init(request):
    json_data = request.data.decode('utf-8')
    post = json.loads(json_data)
    event = WebhookEvent(post)
    rson = event.toRson()
    headers = {'content-type': 'application/json', 'X-Redmine-API-Key': '8d8625c456c6e996de3baaa53065e05204463e02'}
    req = {
        "rson": rson,
        "headers": headers
    }
    return req

def get_issue_id(jira_issue_id, headers):
    r = requests.get(base_url+'/issues.json?status_id=*&cf_4='+jira_issue_id, headers=headers, timeout=3)
    res = json.loads(r.text)
    return str(res.get('issues')[0].get('id'))
    #j = json.loads(r.text)
    return ''
if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=80)

```

Jira의 Webhook 을 이용하여 지라에서 활동한 모든 내용을 레드마인에도 적용이 되는 프로그램 개발을 진행

### 구조

Project, Issue, Comment 3가지 타입으로 나누어 요청에 대한 처리 코드 작성

Builder는 요청에 대하여 redmine에서 요구하는 JSON 값으로 변경하는 역할

WebhookEvent는 Jira에서 발생한 이벤트를 받아서 정리하는 역할

webhook은 메인 클래스로 웹훅의 요청을 받는 클래스


<script id="dsq-count-scr" src="//mcautos-blog.disqus.com/count.js" async></script>
{% if page.comments %}
<div id="disqus_thread"></div>
<script>

/**
*  RECOMMENDED CONFIGURATION VARIABLES: EDIT AND UNCOMMENT THE SECTION BELOW TO INSERT DYNAMIC VALUES FROM YOUR PLATFORM OR CMS.
*  LEARN WHY DEFINING THESE VARIABLES IS IMPORTANT: https://disqus.com/admin/universalcode/#configuration-variables*/
  /*
  var disqus_config = function () {
  this.page.url = PAGE_URL;  // Replace PAGE_URL with your page's canonical URL variable
  this.page.identifier = PAGE_IDENTIFIER; // Replace PAGE_IDENTIFIER with your page's unique identifier variable
  };
  */
  (function() { // DON'T EDIT BELOW THIS LINE
  var d = document, s = d.createElement('script');
  s.src = 'https://mcautos-blog.disqus.com/embed.js';
  s.setAttribute('data-timestamp', +new Date());
  (d.head || d.body).appendChild(s);
  })();
  </script>
  <noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
  {% endif %}