---
layout: post
comments: true
title:  "Golang release, debug 분리하기"
date:   2019-01-24 23:21:00 +0900
categories: back-end
description: go build constraints를 이용하여 release와 debug 버전 분리하기
---
# Golang release, debug 분리하기

[참고 사이트](https://golang.org/pkg/go/build/)

Golang에서 Release와 Debug 버전을 분리하는 방법을 찾던 중 go의 tags옵션을 이용한 코드 분리를 알게 되었다.

사용법은 간단하지만 자료가 없어서 정리를 한다. 누군가는 필요로 할지도 모르겠다.

Java는 gradle, javascript는 npm, python은 pipenv, c++은 cmake또는 make 등을 사용하여 릴리즈 버전과 개발 버전을 다르게 빌드할 수 있다.

go에서도 똑같이 빌드 시에 다른 배포판을 빌드할 수 있는데 이것이 build constraints 이다.

일반적으로 golang으로 패키지를 만들면 다음과 같이 만들 것이다.

**Instance.go**

```go
package mylib

type Instance struct{
    name string
    isDebug bool
}
func NewInstance(name) *Instance{
    return &Instance{name: name, isDebug: false}
}
```

뭔가 예제로는 애매하지만.. 그냥 이런식의 구조체를 설계하고 isDebug 옵션이 true일 경우에는 작동하는 코드들의 내용은 verbose하게 출력할 수 있도록 만든다고 가정하자.

그렇다면 isDebug라는 값을 변경할 수 있어야 하는데, 방법은 대충 2가지 정도인 듯 하다.

1. NewInstance함수의 파라미터에 debug옵션을 추가하여 mylib패키지를 사용하는 곳에서 넘겨주는 방법
2. go build constraints를 사용하는 방법

둘 중에 자신이 편한 것을 사용하면 될 것 같다.

사실 go build constrants는 go의 멀티플랫폼 개발을 지원하기 위해서 사용하는 것 같지만..

> 실제 golang의 공식사이트에서의 설명은 운영체제의 버전으로 설명하고 있다.
>
> 도구의 원래 목적이 어떻든간에 개인적으로 쓰는 사람 마음이라고 생각한다.
>
> ~~컴퓨터도 처음엔 미사일 예측 계산기였지만 지금은 게임기~~
>
> ~~게임의 발전이 없었으면 머신러닝?~~
>
> ~~인터넷의 발전은 사실 19금..~~

1번의 구현은 알아서 할일이라고 생각한다. 하지만 기존의 코드가 있는 경우에는 관련 코드를 다 고쳐야 하지만 2번의 경우는 그냥 함수만 따로 분리하고 NewInstance내부에서 isDebug만 다르게 사용하면 된다. 

코드는 다음과 같다

**Instance-release.go**

```go
// +build release

package mylib

func NewInstance(name) *Instance{
    isDebug := false
    return &Instance{name: name, isDebug: isDebug}
}
```

**Instance-debug.go**

```go
// +build !release

package mylib

func NewInstance(name) *Instance{
    isDebug := true
    return &Instance{name: name, isDebug: isDebug}
}
```

위와 같이 작성한 후에 `go build -tags release`를 입력하면 Instance-release.go의 코드가 빌드되고 Instance-debug.go의 코드는 포함되지 않는다.

`go build` 뿐만 아니라 `go test` 에서도 동일하게 적용되므로 유용한 것 같다.

이것이 이상하지 않은 이유는 package는 하나의 파일로 처리하는 go의 특성인 것 같다.

알면 알 수록 재밌다. ~~한글 자료가 좀 없어서 그렇지~~ 

go의 기본 철학인 `빌드를 편하게 하자`가 뭔지 조금씩 이해가 된다.