---
layout: post
comments: true
title:  "go delve를 이용한 디버깅 하기"
date:   2019-01-21 23:30:00 +0900
categories: back-end
description: go의 gdb delve를 이용하여 디버깅해보자
---

# Go 디버깅 도구 Delve 사용하기

Go로 만들어진 프로그램을 디버깅하기 위한 도구

## 설치방법

```bash
$ go get -u github.com/go-delve/delve/cmd/dlv
```

go를 1.5버전 이상을 설치한 상태에서 위의 명령어를 입력하여 설치가 가능하다.

MacOS, Linux, 윈도우 모두 동일하게 설치 가능하다.

## 사용방법

dlv의 명령어는 [command documentation](https://github.com/go-delve/delve/tree/master/Documentation/cli)이나 다음과 같이 dlv를 입력하면 확인 할 수 있다.

```bash
$ dlv
Delve is a source level debugger for Go programs.

Delve enables you to interact with your program by controlling the execution of the process,
evaluating variables, and providing information of thread / goroutine state, CPU register state and more.

The goal of this tool is to provide a simple yet powerful interface for debugging Go programs.

Pass flags to the program you are debugging using `--`, for example:

`dlv exec ./hello -- server --config conf/config.toml`

Usage:
  dlv [command]

Available Commands:
  attach      Attach to running process and begin debugging.
  connect     Connect to a headless debug server.
  core        Examine a core dump.
  debug       Compile and begin debugging main package in current directory, or the package specified.
  exec        Execute a precompiled binary, and begin a debug session.
  help        Help about any command
  run         Deprecated command. Use 'debug' instead.
  test        Compile test binary and begin debugging program.
  trace       Compile and begin tracing program.
  version     Prints version.

Flags:
      --accept-multiclient   Allows a headless server to accept multiple client connections. Note that the server API is not reentrant and clients will have to coordinate.
      --api-version int      Selects API version when headless. (default 1)
      --backend string       Backend selection:
        default         Uses lldb on macOS, native everywhere else.
        native          Native backend.
        lldb            Uses lldb-server or debugserver.
        rr              Uses mozilla rr (https://github.com/mozilla/rr).
 (default "default")
      --build-flags string   Build flags, to be passed to the compiler.
      --headless             Run debug server only, in headless mode.
      --init string          Init file, executed by the terminal client.
  -l, --listen string        Debugging server listen address. (default "localhost:0")
      --log                  Enable debugging server logging.
      --log-output string    Comma separated list of components that should produce debug output, possible values:
        debugger        Log debugger commands
        gdbwire         Log connection to gdbserial backend
        lldbout         Copy output from debugserver/lldb to standard output
        debuglineerr    Log recoverable errors reading .debug_line
        rpc             Log all RPC messages
        fncall          Log function call protocol
        minidump        Log minidump loading
Defaults to "debugger" when logging is enabled with --log.
      --wd string            Working directory for running the program. (default ".")

Use "dlv [command] --help" for more information about a command.
```

Command가 많지만 가장 기본적인것들부터 써보고 점차 필요에 따라 응용을 해보면서 기록해야겠다.

일반적으로 디버깅 툴을 사용하는 경우는

1. 프로그램이 죽어서 core 파일을 다잉메시지로 남겼을 때
2. 내가 짠 코드가 아닌 남이 짠 코드를 하나하나 실행해 볼 때
3. 내가 짠 코드지만 어떻게 돌아가는지 모를 때
4. 살아있는 프로세스가 버그를 발생시키고 있을 때

정도인 것 같다.

개발 하다가 분명히 사용해서 이해했다고 생각했지만 역시 사람은 망각의 동물이다.

그래서 일단 기록을 해서 한번 더 학습하고자 한다.

1번은 나중에 강제로 에러를 발생시킨 뒤 core파일을 만들어서 한번 남겨서 해봐야겠다.

2,3번은 `debug` 또는 `test` 명령어를 이용하면 되고 4번은 로컬일 경우  `attach` 원격 서버일 경우는 `connect` 인 것 같다.

간단한 예제코드를 이용하여 하나하나 확인해 보자.

프로젝트 구조는 다음과 같다.

```bash
$ tree dlv_practice
dlv_practice
├── main.go
└── mylib
    ├── calc.go
    └── calc_test.go
```

```go
// calc.go
package mylib

// Calc 예제로 만만한건 역시 계산기
type Calc struct {
}

// Add 더하기
func (c *Calc) Add(a int, b int) int {
	result := a + b
	return result
}

```

```go
// calc_test.go
package mylib

import (
	"fmt"
	"testing"
)

func TestAdd(t *testing.T) {
	c := &Calc{}
	var result int
	if result = c.Add(1, 2); result != 3 {
		t.Error(result)
	}
	fmt.Println(result)
}
```

간단하게 계산기 코드 예제를 이용해서 디버깅 테스트를 해보자

dlv의 `test` 명령어를 이용하여 테스트코드의 디버깅을 실행하고

현재 mylib패키지의 테스트코드를 확인하고 싶다면  [`funcs` 명령어](https://github.com/go-delve/delve/tree/master/Documentation/cli#funcs)를 사용하면 된다.

```bash
# cd $GOPATH/src/dlv_practice/mylib
$ dlv test .
(dlv) funcs dlv_practice
dlv_practice/mylib.(*Calc).Add
dlv_practice/mylib.TestAdd
dlv_practice/mylib.init
```

`dlv test .` 를 입력하면 현재 프로젝트를 debug.test를 만들어서 실행시킨다.

```bash
$ ps -ef | grep dlv
501 60328 56979   0 11:14PM ttys002    0:00.11 dlv test .
  501 60351 60328   0 11:14PM ttys002    0:00.02 /Library/Developer/CommandLineTools/Library/PrivateFrameworks/LLDB.framework/Versions/A/Resources/debugserver -F -R 127.0.0.1:58253 -- /Users/mcauto/go/src/dlv_practice/mylib/debug.test
  501 60352 60351   0 11:14PM ttys002    0:00.00 /Users/mcauto/go/src/dlv_practice/mylib/debug.test
```

이제 breakpoint를 걸어서 변수확인과 디버깅을 해보자

breakpoint를 설정하는 방법은[ `break` 명령어](https://github.com/go-delve/delve/tree/master/Documentation/cli#break) 를 이용하여 funcs로 확인한 함수에 걸어보자

```bash
(dlv) b mylib.TestAdd:1 # b: break의 alias
Breakpoint 1 set at 0x1113e2f for dlv_practice/mylib.TestAdd() ./calc_test.go:9
(dlv) c # c: continue의 alias
> dlv_practice/mylib.TestAdd() ./calc_test.go:9 (hits goroutine(5):1 total:1) (PC: 0x1113e2f)
     4:         "fmt"
     5:         "testing"
     6: )
     7:
     8: func TestAdd(t *testing.T) {
=>   9:         c := &Calc{}
    10:         var result int
    11:         if result = c.Add(1, 2); result != 3 {
    12:                 t.Error(result)
    13:         }
    14:         fmt.Println(result)
```

유의할 점으로 함수를 디버깅할 때는 라인 숫자를 상대적으로 입력해서 사용해야 한다.

`c(continue)`를 이용하여 설정한 breakpoint까지 코드를 수행시키면 위와같이 `=>`표시가 왼쪽에 생긴다.

만약에 breakpoint에 도달하지 않을 경우 프로세스는 중단되며, `r(restart)` 명령어를 통해 새로 실행시키면 된다.

해당 포인트의 변수를 확인하기 위해서는 `p(print)` 명령어를 사용하여 변수의 값을 확인할 수 있다.

```bash
$ (dlv) p c
*dlv_practice/mylib.Calc {}
```

한 단계씩 코드를 실행하는 명령어는 `n(next)` 이다.