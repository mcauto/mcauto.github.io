---
layout: post
comments: true
title:  "Network programming 모델에 대하여 알아보기"
date:   2018-11-10 16:41:00 +0900
categories: network
description: TCP, UDP, stateless, stateful, iterative, concurrent 서버에 대하여 알아보자
---
# Network Programming 모델에 대하여 알아보기

Network Programming이란 오늘날의 인터넷 프로토콜(IP; Internet Protocol) 기반을 이용하는 프로그래밍이다.

네트워크 프로그래밍은 OSI 7계층 모형을 기반으로 하며, Client-Server Model을 사용한다.

우리가 사용중인 모든 네트워크 프로그램은 IP 프로토콜 기반 위에 구현되어 있다.

![TCP/IP 관계](http://static.inven.co.kr/column/2016/10/19/news/i12467896678.jpg)


# Client-Server Model

> Server: 서비스를 제공하는 장비
> 
> Client: 서비스를 받는 장비

### Network Program의 흐름

1. Client의 시작 & Server connection 시도
2. 서버로 연결(TCP)후 작업 또는 Request후 response 대기(UDP(Non-Blocking) or HTTP(TCP/UDP))

> 구현 시 주의 사항
> 
> Server는 File system, Port 등의 Resource 관리를 위하여 root 권한을 가지는 경우가 많으므로 
> 
> Client가 Server의 Resource에 Access하지 못하도록 구현해야 함
> 
> 따라서 요청한 Client의 권한을 확인하는 Authentication, Server의 정보 변화에 대한 Security, 다수의 Client에게 서비스를 동시에 제공하는 Concurrency 등을 고려해서 Server를 구현해야 함

### Server와 Client 구현 방법

Client와 Server는 요청과 응답 방식에 따라 나뉜다.

1. 연결형 서버 (TCP), 비연결형 서버 (UDP)
   - OSI 4 layer의 Protocol을 이용한 모델
   - 연결형: TCP 프로토콜, 안정적인 Data 전달, client당 1개의 socket 필요 = 서버 부담 (메모리 문제 야기)
   - 비연결형: UDP 프로토콜, socket 1개로 처리, 전송 후 분실 가능, 서버의 부담이 적음, 브로드캐스팅용
2. stateless 서버, stateful 서버
   - stateful: 통신 상태(state) 추적, 서버 내부 상태 유지를 요구하는 프로토콜, 과거의 동작이 현재의 동작에 영향을 미침, 서버가 reset될 경우 모두 reset 될 가능 성이 높다.
   - stateless: Request가 하나의 트랜잭션으로 처리, Request간 서로 독립적인 처리, 이전 Request에 대한 정보를 이용하여 추가 작업을 할 경우 전송 data의 크기가 커질 수 있다.

3. iterative 서버, concurrent 서버
    - iterative: Request를 순차적으로 처리
        - 하나의 프로세스가 모든 클라이언트의 서비스를 처리
        - 각 서비스의 처리 시간이 짧을 때 사용
        - 서버 프로그램 구현이 단순
    - concurrent: Request를 동시에 처리
        - Client 당 1 Process
        - 각 서비스 처리 시간이 불규칙적이거나 길 때 필요
        - 서버 프로그램 구현이 다소 복잡
        - 각 클라이언트에 대해 프로세스가 하나씩 생성됨.
        - 각 서비스 처리 시간이 불규칙적이거나 길 때 필요