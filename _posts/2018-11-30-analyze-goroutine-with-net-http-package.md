---
layout: post
comments: true
title: "go 작동 분석하기 (on CentOS 7)"
date: 2018-11-30 16:21:00 +0900
categories: back-end
description: strace를 이용하여 go 프로그램의 작동원리 분석하기
---

# go 작동 분석하기 (on CentOS 7)

일단 1초마다 hello world를 출력하는 프로그램을 이용하여 어떤식으로 동작하는지 분석해보자.

## Environment

MacOS (2.2 GHz Intel Core i7) 위에 docker(Version 2.0.0.0-mac81 (29211)를 이용하여 

CentOS 7(2 core / 5G RAM) 사용

사용하는 패키지는 Go에서 기본으로 지원하는 패키지들이다.

## fmt

```go
package main

import (
	"fmt"
	"runtime"
	"time"
)

func main() {
	runtime.GOMAXPROCS(1)

	t := time.NewTicker(time.Second * 1)
	for {
		select {
		case <-t.C:
			fmt.Println("hello world")
		}
	}
	return
}
```

위와 같이 코드를 작성하고 실행시킨 후 다른 터미널을 실행시켜서 process를 확인해보자

```bash
[root@go_practice code] go run analyze.go
hello world
...
```

run command를 이용해서 실행시킬 경우 /tmp/go-build{hash}/command-line-arguments/_obj/exe/{filename}으로 실행이 되며 하나의 프로세스만 뜬 것 처럼 보인다.

```bash
[root@go_practice code] ps -ef | grep analyze
root       675   234  0 06:10 pts/3    00:00:00 go run analyze.go
root       695   675  0 06:10 pts/3    00:00:00 /tmp/go-build915599032/command-line-arguments/_obj/exe/analyze
```

ps의 L옵션을 추가하여 Thread까지 보면 다음과 같이 여러개의 LWP(Light Weight Process)가 돌아가고 있는 것을 볼 수 있다.

> 검색해보니 GOMAXPROCS()는 유저 레벨의 프로세스만 제한을 거는 것 같다.
>
> Kernel scheduler가 생성하는 프로세스들에는 제한 되지 않는 듯 하다.
>
> 참고: https://stackoverflow.com/questions/46974078/runtime-gomaxprocs-not-working-as-expected


```bash
[root@go_practice code] ps -efL | grep analyze
root       675   234   675  0    6 06:10 pts/3    00:00:00 go run analyze.go
root       675   234   676  0    6 06:10 pts/3    00:00:00 go run analyze.go
root       675   234   677  0    6 06:10 pts/3    00:00:00 go run analyze.go
root       675   234   678  0    6 06:10 pts/3    00:00:00 go run analyze.go
root       675   234   679  0    6 06:10 pts/3    00:00:00 go run analyze.go
root       675   234   686  0    6 06:10 pts/3    00:00:00 go run analyze.go
root       695   675   695  0    4 06:10 pts/3    00:00:00 /tmp/go-build915599032/command-line-arguments/_obj/exe/analyze
root       695   675   696  0    4 06:10 pts/3    00:00:00 /tmp/go-build915599032/command-line-arguments/_obj/exe/analyze
root       695   675   697  0    4 06:10 pts/3    00:00:00 /tmp/go-build915599032/command-line-arguments/_obj/exe/analyze
root       695   675   698  0    4 06:10 pts/3    00:00:00 /tmp/go-build915599032/command-line-arguments/_obj/exe/analyze
root       709   146   709  0    1 06:11 pts/2    00:00:00 grep --color=auto analyze
```

strace를 이용하여 각각 어떤식으로 내부에서 작동하고 있는지 확인해보자. 

```bash
[root@go_practice code]# strace -p 675
strace: Process 675 attached
waitid(P_PID, 695, ^Cstrace: Process 675 detached
 <detached ...>
[root@go_practice code]# strace -p 676
strace: Process 676 attached
restart_syscall(<... resuming interrupted futex ...>^Cstrace: Process 676 detached
 <detached ...>
[root@go_practice code]# strace -p 677
strace: Process 677 attached
epoll_wait(4, ^Cstrace: Process 677 detached
 <detached ...>
[root@go_practice code]# strace -p 678
strace: Process 678 attached
futex(0xb05b80, FUTEX_WAIT, 0, NULL^Cstrace: Process 678 detached
 <detached ...>
[root@go_practice code]# strace -p 679
strace: Process 679 attached
futex(0xc420194538, FUTEX_WAIT, 0, NULL^Cstrace: Process 679 detached
 <detached ...>
[root@go_practice code]# strace -p 680
strace: attach: ptrace(PTRACE_ATTACH, ...): No such process
[root@go_practice code]# strace -p 686
strace: Process 686 attached
futex(0xc4202f7938, FUTEX_WAIT, 0, NULL^Cstrace: Process 686 detached
 <detached ...>
```

먼저 run 명령어로 실행된 LWP들을 strace로 내부에서 어떤 동작을 하고있는지 확인해보았다.

내부에서 어떻게 동작하는지는 잘 모르겠으나 각기 프로세스에서 호출하는 함수들을 호출하며 대기하고 있었다.

waitid(), restart_syscall(), epoll_wait(), futex(FUTEX_WAIT)

kill 명령을 통해서 프로세스를 죽이면 실제 실행되고있는 /tmp/go-build LWP 들은 죽지 않고 계속해서 실행된다.

^C 신호를 줘도 계속해서 실행되며 kill 명령어를 통해 프로세스 들 중 아무거나 하나 죽이면 연달아서 전부다 죽었다.

```bash
[root@go_practice code] ps -efL | grep analyze
root       695   675   695  0    4 06:10 pts/3    00:00:00 /tmp/go-build915599032/command-line-arguments/_obj/exe/analyze
root       695   675   696  0    4 06:10 pts/3    00:00:00 /tmp/go-build915599032/command-line-arguments/_obj/exe/analyze
root       695   675   697  0    4 06:10 pts/3    00:00:00 /tmp/go-build915599032/command-line-arguments/_obj/exe/analyze
root       695   675   698  0    4 06:10 pts/3    00:00:00 /tmp/go-build915599032/command-line-arguments/_obj/exe/analyze
root       709   146   709  0    1 06:11 pts/2    00:00:00 grep --color=auto analyze
```

go run의 프로세스는 go-build의 프로세스들에게 사용자 signal을 전달하는 용도인 듯 하다.

```bash
[root@go_practice code]# strace -p 695
strace: Process 695 attached
restart_syscall(<... resuming interrupted futex ...>) = -1 ETIMEDOUT (Connection timed out)
futex(0x53bd38, FUTEX_WAKE, 1)          = 1
futex(0x53bc70, FUTEX_WAKE, 1)          = 1
futex(0xc42002a938, FUTEX_WAKE, 1)      = 1
futex(0x53bb40, FUTEX_WAIT, 0, {0, 997351284} = -1 ETIMEOUT # 여기서 FUTEX_WAIT 하다가 ETIMEOUT이 들어오면 3개의 process를 FUTEX_WAKE시키고 FUTEX_WAIT한다.
^Cstrace: Process 695 detached
 <detached ...>
 
[root@go_practice code]# strace -p 696
strace: Process 696 attached
restart_syscall(<... resuming interrupted futex ...>) = 0
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
futex(0x53bd38, FUTEX_WAIT, 0, {60, 0} # 여기서 대기하다가 pselect6() 의 timeout의 신호를 받고 WAIT을 반복
^Cstrace: Process 696 detached
 <detached ...>
 
[root@go_practice code]# strace -p 697
strace: Process 697 attached
futex(0xc42002a538, FUTEX_WAIT, 0, NULL) = 0
futex(0xc42002a538, FUTEX_WAIT, 0, NULL) = 0
write(1, "hello world\n", 3)                     = 3 # 실제 출력
futex(0xc42002a538, FUTEX_WAIT, 0, NULL
^Cstrace: Process 697 detached
 <detached ...>
 
[root@go_practice code]# strace -p 698
strace: Process 698 attached
futex(0xc42002a938, FUTEX_WAIT, 0, NULL
^Cstrace: Process 698 detached
 <detached ...>
```

이번에는 실제 작동중인 프로세스를 strace로 찍어 보았다.

실제 출력하는 process는 pid 697임을 알 수 있고, 695는 최상위 프로세스로 하위 프로세스를 WAKE함을 알 수 있다.

간단하게 작동하는 구조를 파악했으니 좀더 나아가서 goroutine과 net.http 패키지를 이용해서 확인해보자

## net.http

go에서 기본적으로 지원하는 패키지인 net.http를 통하여 내부에서 어떤식으로 동작하는지 확인해보자.

```go
package main

import (
	"fmt"
	"net/http"
	"runtime"
	"time"
)

func main() {
	runtime.GOMAXPROCS(1) 
	url_list := make(map[string]int)
	url_list["http://www.naver.com"] = 0

	t := time.NewTicker(time.Second * 5)
	for {
		select {
		case <-t.C:
			for url := range url_list {
				go scan(url)
			}
		}
	}
	return
}

func scan(url string) {
	tr := &http.Transport{
		MaxIdleConns:       10,
		IdleConnTimeout:    30 * time.Second,
		DisableCompression: true,
	}
	client := &http.Client{Transport: tr}
	resp, err := client.Get(url)
	if err != nil {
		fmt.Println(err.Error())
	}
	fmt.Println(resp)
}

```

```bash
[root@go_practice code]# ps -efL | grep go
root       469    78   469  0    6 05:50 pts/0    00:00:00 go run http_scan.go
root       469    78   470  0    6 05:50 pts/0    00:00:00 go run http_scan.go
root       469    78   471  0    6 05:50 pts/0    00:00:00 go run http_scan.go
root       469    78   472  0    6 05:50 pts/0    00:00:00 go run http_scan.go
root       469    78   473  0    6 05:50 pts/0    00:00:00 go run http_scan.go
root       469    78   474  0    6 05:50 pts/0    00:00:00 go run http_scan.go
root       490   469   490  0    5 05:50 pts/0    00:00:00 /tmp/go-build622208802/command-line-arguments/_obj/exe/http_scan
root       490   469   491  0    5 05:50 pts/0    00:00:00 /tmp/go-build622208802/command-line-arguments/_obj/exe/http_scan
root       490   469   492  0    5 05:50 pts/0    00:00:00 /tmp/go-build622208802/command-line-arguments/_obj/exe/http_scan
root       490   469   493  0    5 05:50 pts/0    00:00:00 /tmp/go-build622208802/command-line-arguments/_obj/exe/http_scan
root       490   469   500  0    5 05:51 pts/0    00:00:00 /tmp/go-build622208802/command-line-arguments/_obj/exe/http_scan
root       511   234   511  0    1 05:51 pts/3    00:00:00 grep --color=auto go
```

```bash
[root@go_practice code]# strace -p 490
strace: Process 490 attached
futex(0x7bcc38, FUTEX_WAIT, 0, NULL)    = 0
openat(AT_FDCWD, "/proc/sys/kernel/hostname", O_RDONLY|O_CLOEXEC) = 7
futex(0x7bc438, FUTEX_WAKE, 1)          = 1
epoll_ctl(4, EPOLL_CTL_ADD, 7, {EPOLLIN|EPOLLOUT|EPOLLRDHUP|EPOLLET, {u32=3482427056, u64=140453207973552}}) = 0
fcntl(7, F_GETFL)                       = 0x8000 (flags O_RDONLY|O_LARGEFILE)
fcntl(7, F_SETFL, O_RDONLY|O_NONBLOCK|O_LARGEFILE) = 0
read(7, "go_practice\n", 512)           = 12
epoll_ctl(4, EPOLL_CTL_DEL, 7, 0xc4205418dc) = 0
close(7)                                = 0
socket(AF_INET, SOCK_DGRAM|SOCK_CLOEXEC|SOCK_NONBLOCK, IPPROTO_IP) = 7
setsockopt(7, SOL_SOCKET, SO_BROADCAST, [1], 4) = 0
futex(0x7bcc38, FUTEX_WAIT, 0, NULL)    = 0
connect(7, {sa_family=AF_INET, sin_port=htons(53), sin_addr=inet_addr("127.0.0.11")}, 16) = 0
epoll_ctl(4, EPOLL_CTL_ADD, 7, {EPOLLIN|EPOLLOUT|EPOLLRDHUP|EPOLLET, {u32=3482425136, u64=140453207971632}}) = 0
getsockname(7, {sa_family=AF_INET, sin_port=htons(46365), sin_addr=inet_addr("127.0.0.1")}, [16]) = 0
getpeername(7, {sa_family=AF_INET, sin_port=htons(53), sin_addr=inet_addr("127.0.0.11")}, [16]) = 0
write(7, "O7\1\0\0\1\0\0\0\0\0\0\3www\5naver\3com\0\0\34\0\1", 31) = 31
futex(0x7bcc38, FUTEX_WAIT, 0, NULL
^Cstrace: Process 490 detached
 <detached ...>
```



```c
#include <fcntl.h>
int openat(int dirfd, const char *pathname, int flags);
int openat(int dirfd, const char *pathname, int flags, mode_t mode);

#include <sys/epoll.h>
int epoll_ctl(int epfd, int op, int fd, struct epoll_event *event);

#include <unistd.h>
#include <fcntl.h>
int fcntl(int fd, int cmd, ... /* arg */ );

#include <unistd.h>
ssize_t read(int fd, void *buf, size_t count);

#include <unistd.h>
int close(int fd);

#include <sys/types.h>          /* See NOTES */
#include <sys/socket.h>
int socket(int domain, int type, int protocol);

#include <sys/types.h>          /* See NOTES */
#include <sys/socket.h>
int getsockopt(int sockfd, int level, int optname,
               void* optval,socklen_t *optlen);
int setsockopt(int sockfd, int level, int optname,
               const void *optval, socklen_t optlen);
```



```bash
[root@go_practice code]# strace -p 491
strace: Process 491 attached
restart_syscall(<... resuming interrupted futex ...>) = 0
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
futex(0x7bc438, FUTEX_WAIT, 0, {60, 0}) = 0
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
futex(0x7bc438, FUTEX_WAIT, 0, {60, 0}) = 0
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
futex(0x7bc438, FUTEX_WAIT, 0, {60, 0}) = 0
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
futex(0x7bc438, FUTEX_WAIT, 0, {60, 0}) = 0
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
futex(0x7bc438, FUTEX_WAIT, 0, {60, 0}) = 0
sched_yield()                           = 0
futex(0x7bc370, FUTEX_WAIT, 2, NULL)    = 0
futex(0x7bc370, FUTEX_WAKE, 1)          = 0
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
futex(0x7bc438, FUTEX_WAIT, 0, {60, 0}) = 0
sched_yield()                           = 0
futex(0x7bc370, FUTEX_WAKE, 1)          = 0
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
futex(0x7bc438, FUTEX_WAIT, 0, {60, 0}) = 0
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
futex(0x7bc438, FUTEX_WAIT, 0, {60, 0}) = 0
sched_yield()                           = 0
futex(0x7bc370, FUTEX_WAIT, 2, NULL)    = 0
futex(0x7bc370, FUTEX_WAKE, 1)          = 0
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
futex(0x7bc438, FUTEX_WAIT, 0, {60, 0}) = 0
sched_yield()                           = 0
futex(0x7bc370, FUTEX_WAIT, 2, NULL)    = 0
futex(0x7bc370, FUTEX_WAKE, 1)          = 0
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
futex(0x7bc438, FUTEX_WAIT, 0, {60, 0}) = 0
sched_yield()                           = 0
futex(0x7bc370, FUTEX_WAIT, 2, NULL)    = 0
futex(0x7bc370, FUTEX_WAKE, 1)          = 0
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
futex(0x7bc438, FUTEX_WAIT, 0, {60, 0}) = 0
sched_yield()                           = 0
futex(0x7bc370, FUTEX_WAIT, 2, NULL)    = 0
futex(0x7bc370, FUTEX_WAKE, 1)          = 0
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
futex(0x7bc438, FUTEX_WAIT, 0, {60, 0}) = 0
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
futex(0x7bc438, FUTEX_WAIT, 0, {60, 0}) = 0
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
futex(0x7bc438, FUTEX_WAIT, 0, {60, 0}) = 0
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
futex(0x7bc438, FUTEX_WAIT, 0, {60, 0}) = 0
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
futex(0x7bc438, FUTEX_WAIT, 0, {60, 0}) = 0
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
futex(0x7bc438, FUTEX_WAIT, 0, {60, 0}) = 0
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
futex(0x7bc438, FUTEX_WAIT, 0, {60, 0}) = 0
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
futex(0x7bc438, FUTEX_WAIT, 0, {60, 0}) = 0
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
futex(0x7bc438, FUTEX_WAIT, 0, {60, 0}) = -1 EAGAIN (Resource temporarily unavailable)
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
futex(0x7bc438, FUTEX_WAIT, 0, {60, 0}) = 0
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
futex(0x7bc438, FUTEX_WAIT, 0, {60, 0}) = 0
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
futex(0x7bc438, FUTEX_WAIT, 0, {60, 0}) = 0
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
futex(0x7bc438, FUTEX_WAIT, 0, {60, 0}) = 0
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
futex(0x7bc438, FUTEX_WAIT, 0, {60, 0}) = 0
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
futex(0x7bc438, FUTEX_WAIT, 0, {60, 0}) = 0
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
futex(0x7bc438, FUTEX_WAIT, 0, {60, 0}) = 0
pselect6(0, NULL, NULL, NULL, {0, 20000}, NULL) = 0 (Timeout)
futex(0x7bc438, FUTEX_WAIT, 0, {60, 0}
^Cstrace: Process 491 detached
 <detached ...>
```



```bash
[root@go_practice code]# strace -p 492
strace: Process 492 attached
futex(0xc42002c938, FUTEX_WAIT, 0, NULL) = 0
openat(AT_FDCWD, "/proc/sys/kernel/hostname", O_RDONLY|O_CLOEXEC) = 7
futex(0x7bc438, FUTEX_WAKE, 1)          = 1
futex(0x7bc370, FUTEX_WAKE, 1)          = 1
epoll_ctl(4, EPOLL_CTL_ADD, 7, {EPOLLIN|EPOLLOUT|EPOLLRDHUP|EPOLLET, {u32=3482425712, u64=140453207972208}}) = 0
fcntl(7, F_GETFL)                       = 0x8000 (flags O_RDONLY|O_LARGEFILE)
fcntl(7, F_SETFL, O_RDONLY|O_NONBLOCK|O_LARGEFILE) = 0
futex(0xc42002c938, FUTEX_WAIT, 0, NULL^Cstrace: Process 492 detached
 <detached ...>
```



```bash
[root@go_practice code]# strace -p 493
strace: Process 493 attached
epoll_wait(4, [{EPOLLIN|EPOLLOUT, {u32=3482426864, u64=140453207973360}}], 128, -1) = 1
epoll_wait(4, [{EPOLLOUT, {u32=3482426864, u64=140453207973360}}], 128, -1) = 1
epoll_wait(4, [{EPOLLOUT, {u32=3482424560, u64=140453207971056}}], 128, -1) = 1
epoll_wait(4, [{EPOLLIN|EPOLLOUT, {u32=3482426864, u64=140453207973360}}], 128, -1) = 1
epoll_wait(4, [{EPOLLOUT, {u32=3482424560, u64=140453207971056}}], 128, -1) = 1
epoll_wait(4, [{EPOLLIN|EPOLLOUT, {u32=3482424560, u64=140453207971056}}], 128, -1) = 1
futex(0x7bc438, FUTEX_WAKE, 1)          = 1
read(11, "q\1\201\200\0\1\0\3\0\0\0\0\3www\5naver\3com\0\0\1\0\1\300"..., 512) = 97
epoll_ctl(4, EPOLL_CTL_DEL, 11, 0xc420036b14) = 0
close(11)                               = 0
socket(AF_INET, SOCK_DGRAM|SOCK_CLOEXEC|SOCK_NONBLOCK, IPPROTO_IP) = 5
setsockopt(5, SOL_SOCKET, SO_BROADCAST, [1], 4) = 0
connect(5, {sa_family=AF_INET, sin_port=htons(9), sin_addr=inet_addr("210.89.164.90")}, 16) = 0
epoll_ctl(4, EPOLL_CTL_ADD, 5, {EPOLLIN|EPOLLOUT|EPOLLRDHUP|EPOLLET, {u32=3482424560, u64=140453207971056}}) = 0
getsockname(5, {sa_family=AF_INET, sin_port=htons(46349), sin_addr=inet_addr("172.18.0.2")}, [16]) = 0
getpeername(5, {sa_family=AF_INET, sin_port=htons(9), sin_addr=inet_addr("210.89.164.90")}, [16]) = 0
epoll_ctl(4, EPOLL_CTL_DEL, 5, 0xc4200379ac) = 0
close(5)                                = 0
socket(AF_INET, SOCK_DGRAM|SOCK_CLOEXEC|SOCK_NONBLOCK, IPPROTO_IP) = 5
setsockopt(5, SOL_SOCKET, SO_BROADCAST, [1], 4) = 0
connect(5, {sa_family=AF_INET, sin_port=htons(9), sin_addr=inet_addr("125.209.222.141")}, 16) = 0
epoll_ctl(4, EPOLL_CTL_ADD, 5, {EPOLLIN|EPOLLOUT|EPOLLRDHUP|EPOLLET, {u32=3482424560, u64=140453207971056}}) = 0
getsockname(5, {sa_family=AF_INET, sin_port=htons(46987), sin_addr=inet_addr("172.18.0.2")}, [16]) = 0
getpeername(5, {sa_family=AF_INET, sin_port=htons(9), sin_addr=inet_addr("125.209.222.141")}, [16]) = 0
epoll_ctl(4, EPOLL_CTL_DEL, 5, 0xc4200379ac) = 0
close(5)                                = 0
socket(AF_INET, SOCK_STREAM|SOCK_CLOEXEC|SOCK_NONBLOCK, IPPROTO_IP) = 5
setsockopt(5, SOL_SOCKET, SO_BROADCAST, [1], 4) = 0
connect(5, {sa_family=AF_INET, sin_port=htons(80), sin_addr=inet_addr("210.89.164.90")}, 16) = -1 EINPROGRESS (Operation now in progress)
epoll_ctl(4, EPOLL_CTL_ADD, 5, {EPOLLIN|EPOLLOUT|EPOLLRDHUP|EPOLLET, {u32=3482424560, u64=140453207971056}}) = 0
epoll_wait(4, [], 128, 0)               = 0
epoll_wait(4, [{EPOLLOUT, {u32=3482424560, u64=140453207971056}}], 128, -1) = 1
futex(0x7bc438, FUTEX_WAKE, 1)          = 1
getsockopt(5, SOL_SOCKET, SO_ERROR, [0], [4]) = 0
getpeername(5, {sa_family=AF_INET, sin_port=htons(80), sin_addr=inet_addr("210.89.164.90")}, [16]) = 0
getsockname(5, {sa_family=AF_INET, sin_port=htons(37270), sin_addr=inet_addr("172.18.0.2")}, [16]) = 0
setsockopt(5, SOL_TCP, TCP_NODELAY, [1], 4) = 0
read(5, 0xc420352000, 4096)             = -1 EAGAIN (Resource temporarily unavailable)
write(5, "GET / HTTP/1.1\r\nHost: www.naver."..., 71) = 71
epoll_wait(4, [], 128, 0)               = 0
epoll_wait(4, [{EPOLLIN|EPOLLOUT, {u32=3482424560, u64=140453207971056}}], 128, -1) = 1
futex(0x7bc438, FUTEX_WAKE, 1)          = 1
futex(0x7bc370, FUTEX_WAKE, 1)          = 1
read(5, "HTTP/1.1 302 Moved Temporarily\r\n"..., 4096) = 394
futex(0x7bc438, FUTEX_WAKE, 1)          = 1
read(5, "", 4096)                       = 0
epoll_ctl(4, EPOLL_CTL_DEL, 5, 0xc42003797c) = 0
close(5)                                = 0
futex(0xc42002cd38, FUTEX_WAIT, 0, NULL^Cstrace: Process 493 detached
 <detached ...>
```



```bash
[root@go_practice code]# strace -p 500
strace: Process 500 attached
restart_syscall(<... resuming interrupted futex ...>) = -1 ETIMEDOUT (Connection timed out)
futex(0x7bc438, FUTEX_WAKE, 1)          = 1
futex(0x7bc370, FUTEX_WAKE, 1)          = 1
futex(0xc42002c938, FUTEX_WAKE, 1)      = 1
futex(0x7bc0a0, FUTEX_WAIT, 0, {0, 71946313}) = -1 ETIMEDOUT (Connection timed out)
futex(0x7bc438, FUTEX_WAKE, 1)          = 1
futex(0x7bc370, FUTEX_WAKE, 1)          = 1
futex(0xc42002d538, FUTEX_WAKE, 1)      = 1
futex(0x7bc0a0, FUTEX_WAIT, 0, {4, 915189303}^Cstrace: Process 500 detached
 <detached ...>
```



```bash
[root@go_practice code]# clear
[root@go_practice code]# strace -p 636
strace: Process 636 attached
epoll_wait(4, [{EPOLLOUT, {u32=3482427056, u64=140453207973552}}], 128, -1) = 1
epoll_wait(4, [{EPOLLOUT, {u32=3482426096, u64=140453207972592}}], 128, -1) = 1
epoll_wait(4, [{EPOLLIN|EPOLLOUT, {u32=3482426096, u64=140453207972592}}, {EPOLLIN|EPOLLOUT, {u32=3482427056, u64=140453207973552}}], 128, -1) = 2
futex(0x7bc438, FUTEX_WAKE, 1)          = 1
futex(0x7bc370, FUTEX_WAKE, 1)          = 1
read(10, "d7\201\203\0\1\0\0\0\0\0\0\3www\5naver\3com\0\0\34\0\1", 512) = 31
epoll_ctl(4, EPOLL_CTL_DEL, 10, 0xc420037b14) = 0
close(10)                               = 0
read(11, ";e\201\200\0\1\0\3\0\0\0\0\3www\5naver\3com\0\0\1\0\1\300"..., 512) = 97
epoll_ctl(4, EPOLL_CTL_DEL, 11, 0xc420039b14) = 0
close(11)                               = 0
socket(AF_INET, SOCK_DGRAM|SOCK_CLOEXEC|SOCK_NONBLOCK, IPPROTO_IP) = 10
setsockopt(10, SOL_SOCKET, SO_BROADCAST, [1], 4) = 0
connect(10, {sa_family=AF_INET, sin_port=htons(9), sin_addr=inet_addr("210.89.164.90")}, 16) = 0
epoll_ctl(4, EPOLL_CTL_ADD, 10, {EPOLLIN|EPOLLOUT|EPOLLRDHUP|EPOLLET, {u32=3482426096, u64=140453207972592}}) = 0
getsockname(10, {sa_family=AF_INET, sin_port=htons(50175), sin_addr=inet_addr("172.18.0.2")}, [16]) = 0
getpeername(10, {sa_family=AF_INET, sin_port=htons(9), sin_addr=inet_addr("210.89.164.90")}, [16]) = 0
epoll_ctl(4, EPOLL_CTL_DEL, 10, 0xc4203f59ac) = 0
close(10)                               = 0
futex(0xc42002d538, FUTEX_WAIT, 0, NULL) = 0
write(6, "\25\3\3\0\32\0\0\0\0\0\0\0\4\376\214\257|\315\v\334\37\325\246%3\30\1Xi\360L", 31) = 31
epoll_ctl(4, EPOLL_CTL_DEL, 6, 0xc4203f26ac) = 0
close(6)                                = 0
futex(0xc42002d538, FUTEX_WAIT, 0, NULL^Cstrace: Process 636 detached
 <detached ...>
```