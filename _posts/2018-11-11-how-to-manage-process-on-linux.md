---
layout: post
comments: true
title:  "Linux에서 Process를 관리하는 방법"
date:   2018-11-11 19:00:00 +0900
categories: back-end
description: Linux에서 Process를 관리하는 방법
---

# Linux에서 Process를 관리하는 방법

리눅스에서 사용하는 프로그램들은 bin 프로그램과 daemon프로그램이 있다.

bin은 사용자 시점에서 어떤 일을 하기위해서 실행하는 프로그램이고

daemon은 백그라운드에서 계속 실행되고 있는 프로그램이라고 생각하면 이해하기 쉽다.

## Daemon이란?

> Linux 운영체제에서 백그라운드로 돌아가는 프로그램
>
> 주로 postfix로 d가 붙어서 syslogd와 같은 형태의 프로세스
>
본 단어의 뜻은 도깨비, 유령을 뜻하며 MIT의 MAC 프로젝트 프로그래머들이 이름을 붙였다.

유래는 [맥스웰의 도깨비](https://ko.wikipedia.org/wiki/%EB%A7%A5%EC%8A%A4%EC%9B%B0%EC%9D%98_%EB%8F%84%EA%B9%A8%EB%B9%84) [사고 실험](https://ko.wikipedia.org/wiki/%EC%82%AC%EA%B3%A0_%EC%8B%A4%ED%97%98)에서 [맥스웰](https://ko.wikipedia.org/wiki/%EC%A0%9C%EC%9E%84%EC%8A%A4_%ED%81%B4%EB%9F%AC%ED%81%AC_%EB%A7%A5%EC%8A%A4%EC%9B%B0)이 언급한, 보이지 않는 곳에서 분자들을 골라주는 일을 하고 있는 유령에서 영감

## init process

init process는 컴퓨터의 부팅과 동시에 가장 먼저 실행되는 프로세스로 PID가 1이다. (즉 프로세스 넘버원)

리눅스에서는 /sbin/init, MacOS에서는 /sbin/launchd 등으로 실행된다.

이 프로세스를 기준으로 다른 프로세스들은 Child Process가 된다.

`ps -ef`명령어를 입력하면 init 프로세스 외의 프로세스들의 PPID는 대부분 1으로 되어있다.

respawn이 설정된 프로세스가 죽을 경우 init 프로세스가 해당 프로세스를 다시 띄운다.

docker에서 컨테이너를 데몬으로 띄울때 커맨드 명령으로 /sbin/init을 사용해야 하는 경우가 종종있다.(CentOS의 경우)

기본적으로 백그라운드로 돌아가는 프로세스를 관리하기 위해서는 이 init process가 관리할 수 있도록 하는 것이 가장 기본적인 방법이다.

init script 작성하는 방법은 [이곳](https://www.lesstif.com/pages/viewpage.action?pageId=20776215)을 참고하면 좋을 것 같다.

## 대체되는 Init process

**upstart**: Ubuntu의 init process replacement, designed to start process asynchronously

**epoch**: built around simplicity and service management, designed to start process single-threaded.

**mudar**: written in Python, Pardus의 init process replacement,  designed to start process asynchronously

**systemd**: Fedora, OpenSUSE, Arch, RHEL, CentOS의 init process replacement, designed to start process in parallel

검색해보니 위와같은 init process의 대체 프로세스들이 존재했다.

사용해본 프로세스는 upstart와 systemd 두 개 정도 사용해봤고 epoch나 mudar은 이번에 처음 알았다.

잘 쓰고 있던 init process를 바꾸는 이유는 init process의 프로세스 실행 방법때문이다. init process는 serially하게 process를 실행하기 때문에 속도가 느리다. 

하나의 process를 실행한 후 다음 process를 실행하는 방식이기 때문에 프로세스를 추가하면 할 수록 부팅이 느릴 수 밖에 없다.

그래서 최근 리눅스 운영체제에서는 systemd를 이용하여 parallel하게 프로세스를 실행하고 있다. 물론 처음에 실행되는 /sbin/init도 같이 사용하고 있다.

이런 기능 외에 systemd에서는 제공하는 기능들이 다양하지만 이건 [이 글](https://www.tecmint.com/systemd-replaces-init-in-linux/)을 확인하면 좋을 것 같다.

## Linux Programming

> 리눅스에서 사용되는 프로그램을 만드는 것

리눅스에서 사용하는 프로그램은 수행시간이 그리 길지 않은 실행형 프로그램과

컴퓨터를 종료하기 전에 종료되면 안되는 데몬형 프로그램이 있다.

실행형 프로그램의 경우 별다른 관리를 해줄 필요 없지만, 데몬 프로그램의 경우에는 실행 이후 관리가 필요하다.

종료되면 안되지만 프로세스는 언제든지 종료될 위험이 있다.

예를들면 OOM(Out of Memory) killer의 호출이 있다.

이 때 자동으로, 안정적으로, 빠르게 재실행 해주어야 한다.

이 때 systemd는 현재 존재하는 가장 좋은 선택일 것이다.

## 마치며

주로 아이디어의 MVP 개발 위주로 프로그래밍을 했기 때문에 실제 운영적인 부분의 지식이 부족했다.

안드로이드, 웹 백엔드 & 프론트엔드 개발, Arduino, Artik 등 다양하게 사용하면서 일단 실행가능한 프로그램을 만드는 것에 초점이 주로 잡혀있었고, 

아이디어를 구현하는 것 자체에는 별다른 거부감이 없었으나 매번 배포에 대해서는 막연한 방식을 생각했었다.

그러나 최근 실제 현업에서 개발과 배포 및 운영을 하면서 공부했던 내용을 정리해야겠다고 생각이 들었다.

머리로 이해하는 것과 글로 정리하는 것은 확실히 다른 듯 하다.

