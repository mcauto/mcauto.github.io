---
layout: post
comments: true
title: "OpenTSDB 사용하기"
date: 2019-01-09 23:00:00 +0900
categories: infra
description: 모니터링을 위한 시계열 데이터베이스 OpenTSDB 간단하게 사용하기
---

## OpenTSDB란?

OpenTSDB란 Open source Time Series Database(오픈소스 시계열 데이터베이스)이다.

코드는 [GitHub repo](https://github.com/OpenTSDB/opentsdb)에서 확인할 수 있다.

README를 간단하게 해석해보면 

> OpenTSDB는 Hbase 위에서 작성된 분산, 확장 가능한 Time Series Database이다.
>
> OpenTSDB는 운영체제, 네트워크 장비, 응용프로그램으로부터 수집된 대규모의 메트릭의 저장, 인덱스, 전달하고자하는 필요에 의해서 만들어졌다. 그리고 이런 데이터는 쉽게 접근가능하고 도식화가 가능하다.
>
> Hbase의 확장성 덕분에 OpenTSDB는 수만 개의 호스트 및 응용프로그램에서 수천 개의 metric을 고속으로(매 초마다) 수집할 수 있다.
>
> OpenTSDB는 데이터를 삭제하거나 다운샘플링하지 않으며 수십억 데이터 포인트를 쉽게 저장할 수 있다.



![tsdb-architecture](http://opentsdb.net/img/tsdb-architecture.png)

공식 사이트에서 제공하는 이미지를 통해 작동 원리를 알 수 있다.

실제 작동원리는 위와같이 수집 대상인 server 또는 network 장비들에서 collector가 TSD(Time Series Daemon)로 전송하면 TSD가 HBase에 저장하도록 설계 되어 있다.

OpenTSDB는 HTTP API, Web UI, Telnet 등으로 HBase에 읽고 쓰기를 지원한다.

모든 접근은 동일한 포트(일반적으로 4242)에 접근하며 처음 몇 바이트를 조사하여 요청한 클라이언트의 프로토콜을 파악하여 처리한다.

TSDB에 저장되는 기본적인 데이터포맷은 다음과 같다.

- Metric name
- Unix timestamp(Epoch)
- a Value(int64, float, JSON)
- A set of tags

Metric name은 key값으로 hashtable의 key로 생각하면 된다.

Unix timestamp는 수집 시간

value는 해당 메트릭의 값

tags는 해당 메트릭의 추가 정보, 말 그대로 key-value로 이루어진 태그의 집합이다.

주로 검색 및 aggregation 할 때 사용된다.

## 그래서 OpenTSDB란?

결국 데이터를 저장하기 위한 데이터베이스이다.

대용량의 데이터를 쉽고 빠르게 읽고 쓰기가 가능한 storage가 필요해서 만들어진 것

## 사용하기

백문이 불여일견이라는 말이 있듯이 일단 사용해보면 감이 잡힌다.

엄청난 기술의 집약체인 스마트폰도 우리는 그냥 사용한다.~~제대로 쓰고 있는지는 알 수 없지만~~

OpenTSDB도 실제로 production에서 사용하려면 많은 설정과 세팅이 필요하다. 설정 이후에도 opentsdb의 수집 방식에 따라 모니터링 및 관리가 필요하다.

하지만 단순히 공부(?)를 위해서라면 docker가 있다.

docker hub에 검색하면 official은 아니지만 100K+의 다운로드를 받은 컨테이너들이 다수 보인다. 

![image-20190108230415102](/assets/img/docker_hub_opentsdb.png)

가장 최신에 업데이트 된 petergrace/opentsdb-docker의 이미지를 받아서 실행하면 gnuplot 버전으로 인해서 실행이 안된다.

opentsdb에 가서 [이슈](https://github.com/OpenTSDB/opentsdb/issues/1421)를 남겼더니 3.0 브랜치 기준으로 만들어진 dockerfile가 있었다. 

docker hub에 official로 안올리는 이유는.. 잘 모르겠다.

3버전을 사용하기에는 공식문서가 2버전으로 stable을 지원하고 있어서 petergrace/opentsdb-docker의 PR에 6개월동안 올라와있는 [수정된 repo](https://github.com/jlferrer/opentsdb-docker)를 이용하여 실행할 수 있다.

```bash
$ git clone https://github.com/jlferrer/opentsdb-docker.git
$ cd opentsdb-docker
$ docker-compose up -d # docker-compose 없을 시 설치
Pulling opentsdb (petergrace/opentsdb-docker:latest)...
..
Creating opentsdb-docker_opentsdb_1 ... done
```

위와 같이 프로젝트를 받아서 도커를 실행할 수 있다.

```bash
http://localhost:4242
```

로 접속하면 다음과 같은 화면을 볼 수 있다.

![opentsdb_web_ui](/assets/img/opentsdb_web_ui.png)

이제 설치를 다했으므로 [HTTP API](http://opentsdb.net/docs/build/html/api_http/index.html)를 통하여 데이터를 저장해보자.

```json
{
    "metric": "sys.cpu.nice",
    "timestamp": 1546957946,
    "value": 18,
    "tags": {
       "host": "deo"
    }
}
```

위의 데이터를

```http
@POST 
http://localhost:4242/api/put?details
```

위의 주소로 요청을 보내면 (Postman 사용)

![opentsdb_write](/assets/img/opentsdb_write.png)

데이터가 저장이 된다.

저장된 데이터의 확인은 아래의 요청으로 가능하다.

```http
@GET
http://localhost:4242/api/query?start=1h-ago&m=sum:sys.cpu.nice
```

![opentsdb_read](/assets/img/opentsdb_read.png)

#### [예제 프로젝트](https://github.com/mcauto/opentsdb-practice)