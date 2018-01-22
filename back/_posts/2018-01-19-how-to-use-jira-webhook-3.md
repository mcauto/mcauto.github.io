---
layout: post
comments: true
title:  "Redmine, Jira 같이 사용하기 4"
date:   2018-01-19 18:16:00 +0900
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
		return 'raise NotImplementedError()'

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
			"project": {
				"name": e.name,
				"identifier": e.key,
				"description": ''
			},
			"type":"POST"
		}
		return create_json

	def update(self):
		e = self.event

		update_json = {
			"project": {
				"name": e.name,
				"identifier": e.key,
				"description": ''
			},
			"type":"PUT"
		}
		return update_json

	def delete(self):
		e = self.event
		delete_json = {
			"project": {
				"identifier": e.key,
				"description": ''
			},
			"type":"DELETE"
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
			"issue":{
				"project_id":e.issue_proj_key,
				"priority_id":e.issue_priority,
				"status_id":1,
				"subject":e.issue_summary,
				"description":e.issue_description,
				"assigned_to_id":1,
			},
			"type":"POST"
		}
		return "issue create"

	def update(self):
		update_json = {
			"issue":{
				"project_id":e.issue_proj_key,
				"priority_id":e.issue_priority,
				"status_id":1,
				"subject":e.issue_summary,
				"description":e.issue_description,
				"assigned_to_id":1,
			},
			"type":"PUT"
		}
		return "issue update"

	def delete(self):
		delete_json = {
			"issue":{
				"id":e.issue_id
			},
			"type":"DELETE"
		}
		return "issue delete"


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
			"issue":{
				"project_id":"",
				"priority_id":"",
				"status_id":"",
				"subject":"",
				"description":"",
				"assigned_to_id":"",
			},
			"type":"POST"
		}
		return "comment create"

	def update(self):
		update_json = {
			"issue":{
				"project_id":"",
				"priority_id":"",
				"status_id":"",
				"subject":"",
				"description":"",
				"assigned_to_id":"",
			},
			"type":"PUT"
		}
		return "comment update"

	def delete(self):
		delete_json = {
			"issue":{
				"project_id":"",
				"priority_id":"",
				"status_id":"",
				"subject":"",
				"description":"",
				"assigned_to_id":"",
			},
			"type":"DELETE"
		}
		return "comment delete"

```

### WebhookEvent.py

```Python
from Builder import *


class WebhookEvent:
  def __init__(self, dict):
    self.webhookEvent = dict.get('webhookEvent', None)
    self.issue_event_type_name = dict.get('issue_event_type_name', None)
    self.changelog = dict.get('changelog', None)
    self.isProject = 'project' in dict
    self.isComment = 'comment' in dict and self.issue_event_type_name == None
    if self.issue_event_type_name != None:
      self.isIssue = ('issue' in dict) and ('comment' not in dict) and self.issue_event_type_name.find('comment')
    else:
      self.isIssue = ('issue' in dict) and ('comment' not in dict)

    if self.isProject:
      self.proj = dict.get('project',None)
      self.proj_key = self.proj.get('key',None)
      self.proj_name = self.proj.get('name',None)
      self.projectLead = self.proj.get('projectLead',None)
      self.author = '' if self.projectLead == None else self.projectLead.get('name')
    elif self.isComment:
      pass
    elif self.isIssue:
      self.issue = dict.get('issue',None)
      self.issue_id = self.issue.get('id',None)
      self.issue_key = self.issue.get('key',None)
      self.issue_fields = self.issue.get('fields',None)
      self.issue_proj = self.issue_fields.get('project',None)
      self.issue_proj_key = self.issue_proj.get('key',None)
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

@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        json_data = request.data.decode('utf-8')
        post = json.loads(json_data)
        event = WebhookEvent(post)
        result = event.toRson()
        headers = {'content-type': 'application/json', 'X-Redmine-API-Key': 'your-api-key'}
        if is_json(result):
            r = requests.post('http://redmine_server:3000/issues.json', headers=headers, data=json.dumps(result))
            r = requests.post('http://1c4fc821.ngrok.io', headers=headers, data=json.dumps(result))

    return ''

def is_json(myjson):
    try:
        json_object = json.dumps(myjson)
    except ValueError as e:
        return False
    return True

@app.route('/del_pro',methods=['POST'])
def del_pro():
    json_data = request.data.decode('utf-8')
    post = json.dumps(json_data)
    headers = {'content-type': 'application/json'}
    requests.delete('http://redmine_server:3000/projects/'+json_data['project_id']+'.json',header=headers)

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