---
layout: post
comments: true
title:  "Redmine, Jira 같이 사용하기"
date:   2018-01-17 20:00:00 +0900
categories: back-end
---
# Jira Webhook 사용하기

## Webhook

- 사용자 정의 HTTP callback
- 특정 이벤트 발생 시 작동
- REST API를 통해 주기적으로 확인 가능

## 개요

- 이름
- 목적지 URL
- 범위(issue, JQL)
- Event

아래와 같이 생김

```Bash
Name: "auto's webhook"
URL: www.myremoteapp.com/webhookreceiver
Scope: all issues
Events: all issue events
```

또는

```Bash
Name: "auto's more advanced webhook"
URL: www.myremoteapp.com/webhookreceiver
Scope: Project = JRA AND fixVersion IN ("6.4", "7.0")
Events: Issue Updated, Issue Created
```

## 설정 위치

 **JIRA 관리 > 시스템 > 왼쪽 메뉴 중 고급 > 웹훅** 또는 키보드입력 **`g`+`g`+`웹훅`**



## 사용하기 예제

참고: [Tutorial: Create and Trigger a Webhook](https://confluence.atlassian.com/bitbucket/tutorial-create-and-trigger-a-webhook-747606432.html)

```Bash
git clone your-github-id@bitbucket.org:atlassianlabs/webhook-listener.git
cd webhook-listener
# pip2로 설치해야함 python2 기준으로 만들어진 프로젝트
pip install -r requirements.txt	
```

pip2로 설치하지 않으면 python2 와 python3의 print 함수 차이로 인한 listener.py 파일의 print 구문 에러와 pync 모듈을 찾을 수 없다는 오류를 만날 수 있음

```Bash
# .env
NGROK_SUBDOMAIN=<first_name> # ngrok 사용할때 앞에 붙을 도메인 이름
```

ngrok free 버전은 subdomain을 사용할 수 없으므로 파일을 아래와 같이 수정

```Bash
# .Procfile
listener: PYTHONUNBUFFERED=true python listener.py
tunnel: ngrok http 80 #-log stdout -subdomain=0e6dc686
```

그리고 실행 했을 때 아래와 같이 나오면 성공

```Bash
honcho start
15:44:18 system     | listener.1 started (pid=3235)
15:44:18 system     | tunnel.1 started (pid=3237)
15:44:18 listener.1 | You can access this webhook publicly via at http://mcauto.ngrok.io/webhook.
15:44:18 listener.1 | You can access ngrok's web interface via http://localhost:4040
15:44:18 listener.1 |  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
15:44:18 listener.1 |  * Restarting with stat
15:44:19 listener.1 | You can access this webhook publicly via at http://mcauto.ngrok.io/webhook.
15:44:19 listener.1 | You can access ngrok's web interface via http://localhost:4040
15:44:19 listener.1 |  * Debugger is active!
15:44:19 listener.1 |  * Debugger PIN: 132-367-584
```

http://localhost:4040 에 접속하면 브라우저에서 아래와 같은 주소를 확인할 수 있다.

```Bash
No requests to display yet
To get started, make a request to one of your tunnel URLs
http://1c4fc821.ngrok.io
https://1c4fc821.ngrok.io
```

이후 접속하는 모든 GET, POST, PUT, DELETE의 정보를 확인 할 수 있다

개인적으로 postman을 써서 확인을 많이 했지만 ngrok을 사용해서 개발하면 따로 코드 작성 없이 확인 할 수 있을 것으로 판단됨



## 개발 중 일어난 문제

#### post.json 

```http
@Post 
http://localhost
```

```json
{
  "title":"hi"
  "description":"data"
}
```

POSTMAN은 성공 JIRA Webhook은 실패

JIRA Webhook이 전송이 제대로 되는지 확인하기 위해 ngrok을 사용해 봄

## 문제 해결책

JIRA container, Webhook receiver container간의 localhost 차이 때문

JIRA container에서 웹훅 주소를 localhost로 하면 JIRA 자기자신에게 계속 요청

따라서 Webhook receiver container의 IP주소로 Request 

또는 각각의 container에 --link를 적용하여 해결



하루종일 이 문제로 고생함

개발환경은 내장 서버를 사용하는 것이 훨씬 유용

gunicorn, uWSGI는 배포용

### 요청에 대한 결과를 실시간으로 콘솔에 찍어주는 내장 서버 만세

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