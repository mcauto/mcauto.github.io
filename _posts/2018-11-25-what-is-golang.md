---
layout: post
comments: true
title:  "Golang 내용 정리"
date:   2018-11-25 01:11:00 +0900
categories: back-end
description: Golang 내용 정리
---
# Golang 내용 정리

최근에 Golang으로 네트워크 프로젝트를 진행하고 있어서 공부 및 정리를 하려고 한다.

이 글은 아무래도 프로젝트 하는 기간 동안 자주 수정하게 될 듯 하다.

추가로 프로젝트에 사용한 패키지를 분석하는 글과 Repo를 올릴 예정이다.

최근에 사용한 패키지는 [viper](https://github.com/spf13/viper), [beego/orm](https://github.com/astaxie/beego/tree/develop/orm), [daemon](https://github.com/takama/daemon), [go-fastping](https://github.com/tatsushid/go-fastping), [net](https://github.com/golang/net)이 있다.

처음 시작할때 도움이된 패키지는 go-fastping이다. icmp를 이용하여 ping체크를 하는 라이브러리인데 비동기처리가 잘되어있어서 공부에 많은 도움이 되었다.

## Golang이란?

Golang은 google에서 만든 open source programming language.

2009년에 release 되었으며 9살(한국나이는 10살; 현재 2018년) 먹은 언어다. 현재 golang의 major 버전은 1이고 향후 5년간 버전 2를 위해 개발할 예정.

Golang으로 프로젝트를 시작하게 된 계기는 고루틴과 강력한 기본 패키지들과 단순한 문법 때문이었다.

처음 언어가 시작된 모토가 C와 C++은 사용하기 너무 어려우니 더 쉽게 언어를 만들자~~(세종대왕님?)~~인 만큼

언어의 문법은 엄청 단순하다. 

상속, 제네릭, 메서드 오버로딩, 포인터 연산 등이 일절 없다. (STL container도 없다. 그러나 구현된 패키지는 github에 널렸다. 아마도 오픈소스를 지향하는 언어인 만큼 개발자들에게 넘긴듯 하다.)

인터페이스는 존재하지만 implement가 아닌 satisfy로 표현하는 만큼 강제적이지 않다.

언어 자체가 계층을 지양하는 터라 코드를 분석하기가 다소 편하다.

이 언어의 핵심 및 목적은 다음과 같다고 한다. (위키에서 발췌)

1. 안전성: 타입 안전성과 메모리 안전성

2. 병행성과 통신을 위한 훌륭한 지원

3. 효과적인 가비지 컬렉션

4. 빠른 컴파일

현재 프로젝트에서 사용한지 얼마되지 않았고 프로젝트를 위해서 사용하는 만큼 다 겪어보지는 못했지만 개발 및 테스트를 통해 겪은 짧은 경험을 기록하고자 한다.

#### 안전성

변수 선언 및 정의, 패키지 import 등에 다소 강제적이다.

사용하지 않는 변수가 있는 경우 컴파일 에러가 발생하며, 패키지 또한 동일하다.

그래서 IDE에서는 사용하지 않는 패키지는 자동으로 사라진다.(개발 도중에 주석처리할 때 좀 불편하다.)

#### 병행성(concurrency)과 통신(network)을 위한 훌륭한 지원

병행성(또는 동시성)은 확실히 좋다.

기존의 쓰레드의 메모리 사용과 컨텍스트 스위칭에 사용되는 비용에 비해서, 매우 적은 비용으로 쓰레드를 생성해서 사용한다. 자세한 내용 은 [이 글](https://stonzeteam.github.io/How-Goroutines-Work/)을 참고하면 좋을 것 같다.

링크를 요약하자면 

```
Thread: 1MB, 16 GPR, PC, SP, SR, 16 XMM, FP, 16AVX, MSR
Goroutine: 2KB, PC, SP
```

각각 1개에 사용되는 서버 Resource라고 한다.

통신은 [net](https://godoc.org/net) 패키지를 사용해보는 것이 좋을 것 같다.

또는 [go-fastping](https://github.com/tatsushid/go-fastping/blob/master/fastping.go)의 코드를 분석하면서 사용해보는 것도 좋을 것 같다. 

네트워크 쪽은 실제로 프로젝트를 진행해본 경험이 없어서 아직은 표현하기는 이른 듯 하다.

하지만 goroutine은 확실히 사용하면서 좋다고 느꼈다.

> goroutine은 M:N thread이며 LWP(Light Weight Process)로 구현되어 있다고 한다. 
>
> 이론은 파면 팔수록 계속해서 쏟아져 나온다.
>
>  [goroutine vs threads](https://tech.ssut.me/goroutine-vs-threads/) 설명이 잘 되어 있다.
>
> [사용자수준 쓰레드와 커널수준 쓰레드의 차이?](https://kldp.org/node/295) 이건 좀 전투적인 글 댓글이 콜로세움이다.



#### 효과적인 가비지 컬렉션

가비지 컬렉션 이야기가 나왔는데 고언어는 가비지 컬렉션을 제공하지만 VM(Virtual Machine)은 아니다.

VM이라 하면 Java, C#, Python 등이 대표적으로 생각난다. 

언어가 빌드되면 해당 VM의 바이트 코드로 변환, VM의 Loader에서 memory에 할당하는 작업을 한다.

Go는 C처럼 complie and go 방식으로 빌드 되는 순간 memory에 올라가기 위한 전처리를 다 끝내고 binary 파일을 만들어 낸다.

가비지 컬렉션이 있다고 하더라도 **close 함수가 있는 패키지의 경우에는 `defer`를 이용한 close는 필수**

#### 빠른 컴파일

**개발측면**

컴파일이라고하면 C와 C++에서는 `Makefile`이 가장 먼저 생각날 것이다.

golang은 그런거 필요없이 `go build` 명령어 하나면 바이너리 파일이 생성된다.

**컴파일 측면**

의존성 해석 알고리즘을 통하여 사용하는 라이브러리만 컴파일한다.

> ### Go build
>
> Golang에서 빌드 할 때 다음과 같은 옵션을 주면 디버깅 symbol을 제거한 바이너리를 생성하여 용량을 줄일 수 있다.
>
> [참고](https://groups.google.com/forum/#!msg/golang-korea/bP3ejliyiqQ/igHLKFBfX1gJ)
>
> ```bash
> $ go build -ldflags "-s"
> ```

