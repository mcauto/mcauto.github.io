---
layout: post
comments: true
title:  "Golang 문법 정리"
date:   2018-10-29 22:00:00 +0900
categories: back-end
description: Golang 문법 정리
---

# Golang 문법 정리

http://golang.site/

고 언어 정리 - 빠르게 훑어보기용

## 변수

>  var {변수명} {자료형}

1. 변수는 생성시 Zero Value(0, false, "")를 default로 가진다. 

2. Short Assignment Statement (:=)를 사용한 변수 선언 가능

   > var i = 1 또는 i := 1

3. 함수 밖에서는 var로 변수 정의

## 상수

> 1. const {변수명} {자료형}
>
> 2. const (
>
>    ​	{변수명} = {값}
>
>    )
>
> 3. const (
>
>    ​	{변수명} = iota // 0부터 auto increase
>
>    ​	{변수명2}
>
>    )

## Go 키워드

```go
break        default      func         interface    select
case         defer        go           map          struct
chan         else         goto         package      switch
const        fallthrough  if           range        type
continue     for          import       return       var
```

위의 키워드는 함수, 변수, 상수 이름으로 사용할 수 없다.

## 문자열

> 여러줄 사용(Raw String): `(Back Quote)
>
> 한줄 사용(Interpreted String Literal): "(Double Quote)

## 형 변환

> var i int = 100
>
> var u uint = uint(i)

다른 언어와 동일, 하지만 반드시 명시적 형 변환 사용

## 연산자

`+ - * / % ++ -- == != <= && || ! << += &`

다른 언어와 동일하다.

## if 조건문

> if i == 1 { 실행할 코드 }
>
> else if i == 2 { 실행할 코드 }
>
> else { 실행할 코드 }

1. 특이하게 괄호 를 안씀

2. 반드시 boolean

3. 조건식에 코드 삽입가능

   ```go
   if value := i*2; value < max {
       println(value)
   }
   value++ // Error, 변수는 block scope
   ```

## Switch 조건문

> switch {변수 또는 표현식} {
>
> case {value}:
>
> default:
>
> }

1. break 없어도 됨

2. 표현식 사용 가능

   ```go
   // 0 0 0 1
   // 8 4 2 1
   category := 1
   
   switch x := category << 2; x {
   	case 1:
       case 4:
       println("hello")
   }
   ```

3. switch 다음에 변수나 표현식이 없어도 됨
4. case 중첩안됨 (fallthrough 키워드 사용하면 가능)
5. case 조건식 가능
6. case 자료형 가능

## 반복문

> for 정의 ; 조건문 ; 증감 { 실행할 코드 }
>
> for 조건문 { 실행할 코드 }
>
> for { 무한루프 }
>
> for 인덱스, 값 := range 컬렉션 { 실행할 코드 }
>
> break, continue, goto 존재
>
> 특이하게 break를 goto처럼 사용가능

## 함수

>func 함수명 ( 파라미터 ) { 실행할 코드}
>
>func (msg …string) { 실행할 코드 } // string은 가변인자
>
>func 함수명 (nums ...int) ( 반환 자료형 ... ) { 실행할 코드 } // return이 없더라도 return 필수

pass by value, pass by reference: c언어의 call by value, address와 동일

return 값이 복수 개

## 익명 함수

> 변수 := func ( 파라미터 )  반환 자료형  { 실행할 코드 }

## 일급 함수

함수를 다른 함수의 파라미터로 전달 가능

## 함수 원형 정의

> type 원형 함수명 func ( 파라미터 ) 반환 자료형 // 선언하고
>
> func 함수명 (f 원형 함수명, 파라미터) 반환 자료형 { 실행할 코드 } // 정의한다.

함수의 원형을 미리 정의하고 함수를 다른 함수에 전달하고 구현한 뒤 리턴 하는 방식

델리게이트( Delegate; 위임 )이라고 부름

선언하고 정의하는 과정에서 변수와 비슷

## 클로저

> func 함수명 () func() int {
>
> ​	i:=0
>
> ​	return func() int {
>
> ​		i ++
>
> ​		return i
>
> ​	}	
>
> }

함수를 리턴하는 함수

리턴된 함수는 처음에 호출한 함수의 변수들을 사용할 수 있다.

## 배열

> var 변수명 [개수] 자료형
>
> var 변수명 […] 자료형 {1,2,3} // 배열크기 자동처리
>
> 대괄호 두개로 다차원 배열 가능

## Slice

> var 변수명 []자료형  // 크기 입력 안할 시 slice 변수로 선언됨
>
> 변수명 := make([]자료형, Length, Capacity)
>
> 변수명[n:m] // n부터 m까지 잘라낼 수 있다. [:]은 전체
>
> 변수명 = append(변수명, 추가 요소) // 자유롭게 추가 가능

Length(길이)와 Capacity(용량)를 표현하는 가변크기 배열

append 시 capacity가 부족할 경우 현재 capacity의 2배를 생성한 뒤 복제하여 전부다 migrate한다. (비용발생)

slice 두 개를 append할 경우 두 번째 파라미터는 `…`을 추가한다.

슬라이스의 내부구조는 배열을 가리키는 노드이다. (포인터, length, capacity) 구조를 지닌다.

즉 용량이 초과할경우 슬라이스의 포인터는 새로 할당된 영역의 첫 주소를 가리키며

기존의 데이터를 이어서 복사한다.

## Map

> 변수명 := map[자료형]자료형

Key와 Value를 가지는 자료형

map에 Key가 존재하지 않을 경우 nil( reference 자료형 ) 또는 Zero value를 반환

key 존재 여부 확인방법

```go
value, exists := tickets["twice"]
if !exists {
    println("No twice ticket")
}
```

Map iterate

```go
tickets := map[string]int{
    "twice": 0,
    "exhibition": 2
}
for key, value := range tickets{
    fmt.Println(key, value)
}
```

## Package

> 가장 작은 단위의 Component
>
> 기본 패키지: $GOROOT/pkg
>
> 메인 패키지: main - 컴파일러가 실행 프로그램으로 인식하는 Entry point
>
> 그 외 패키지: GOROOT또는 GOPATH 환경변수 기준으로 검색

**패키지 Scope**

대문자는 public, 소문자는 패키지에서만 사용 가능

**패키지 init 함수와 alias**

init은 패키지 호출 시 실행

alias는 이름이 동일한 경우 구분할 때 사용

**패키지 생성 방법**

폴더 생성 후 go 파일 생성

패키지명은 폴더명과 반드시 동일해야 함

해당 폴더의 go파일은 하나의 패키지로 묶여서 사용

사이즈가 큰 복잡한 라이브러리의 경우 `go install` 명령을 사용하여 캐싱 가능

## 구조체 Structure

> Custom Data Type
>
> Field의 집합체이자 컨테이너
>
> 다른 언어와 달리 메서드를 갖지 않음
>
> 일반적인 객체지향 언어와 다른 방식으로 지원
>
> 메서드는 별도로 분리하여 정의

```go
package main
import "fmt"
type Person struct{
    name string
    age int
}

func main(){
    p := Person{}
    p.name = "Name"
    p.age = 100
    fmt.Println(p)
}
```

**객체 생성 방법**

```go
var p1 Person // 변수 선언
p1 = Person{"name", 100} // 특이하게 중괄호 사용
p2 := Person{name:"name", age: 100} // dictionary 처럼 사용 가능
p := new(Person) // 객체의 pointer를 반환하는 new 함수
p.name = "Name"	// pointer도 .(dot) 연산자로 접근 가능
```

기본적으로 Go의 Struct는 mutable으로 메모리에서 직접 변경

그러나 func의 param으로 넘길 경우 주소가 아닌 값을 전달 (Pass by value)

**생성자 함수**

생성자가 없으므로 직접 구현해주어야 한다

```go
package main
type Dict struct{
    data map[int]string
}
func newDict() *Dict{
    d := Dict{}
    d.data = map[int]string{}
    return &d	//포인터 반환
}
func main(){
    dic := newDict() // 생성자 호출
    dic.data[1] = "A"
}
```

## Go method

> Go의 객체지향 프로그래밍을 위한 기법
>
> 필드만 정의된 struct에 함수를 정의하여 구현
>
> type 구조체명 struct{
>
> ​	변수명 자료형
>
> }
>
> func (변수명 구조체명) 메소드명() 반환형 {
>
> ​	return 반환값
>
> }

메소드를 포인터를 이용하여 구현하면 **값 변경시 다른 값들도 변경**된다.

## Go interface

> Struct는 field의 집합체
>
> Interface는 method의 집합체
>
> 다른 언어의 최상위 객체와 동일
>
> type 인터페이스명 interface{
>
> ​	함수명() 반환형
>
> }

인터페이스의 메소드를 다른 구조체에서 구현할 경우

Interface를 이용하여 다형성 구현이 가능

**Interface type**

```go
func 함수명(v interface{}) (n int, err error);
```

interface는 어떠한 값도 담을 수 있는 컨테이너 역할을 한다. (Java의 Object, C++의 void*)

**Type assertion**

interface의 자료형을 강제하는 기법

```go
var a interface{} = 1
i := a			// a와 i는 동적 타입, 값은 1 
j := a.(int) 	// j는 int형, 값은 1
println(i) 		// 주소값 출력
println(j)		// 1 출력
```

## Go Error

> Go에서 Error는 내장 타입, 제일 빈번하게 사용
>
> type error interface{
>
> ​	Error() string
>
> }

```go
package main
import (
    "log"
    "os"
)
func main(){
    f, err := os.Open("filename.txt")
    if err != nil { // 가장 흔한 에러 처리 - 1
        log.Fatal(err.Error())
    } 
    switch err.(type){	// type을 체크하여 처리 - 2
        default:
    case MyError:
        log.Print("My Error")
    case error:
        log.Fatal(err.Error())
    }
    println(f.Name())
}
```

2번 방법보다는 그냥 error interface의 Error() 함수를 override 하여 반환하는 편이 좋을 것 같다.

## Go defer, panic, recover()

> return 직전에 수행되는 가장 마지막 호출 함수 키워드 `defer`
>
> 에러 발생 시 현재 로직을 즉시 중단 하고 defer를 모두 실행시킨 후 강제로 종료 하는 키워드 `panic`
>
> panic 상태에서 정상상태로 돌린 후 다음 로직을 수행하게 하는 함수 `recover()`

## Goroutine

> Go 런타임이 관리하는 경량 쓰레드
>
> 호출 방법은 함수 앞에 `go` 키워드만 붙이면 끝
>
> **Goroutine**
>
> > OS 쓰레드보다 훨씬 가볍게 비동기 Concurrent 처리를 구현하기 위하여 만든 것으로, 기본적으로 Go 런타임이 자체 관리한다. Go 런타임 상에서 관리되는 작업단위인 여러 goroutine들은 종종 하나의 OS 쓰레드 1개로도 실행되곤 한다. 즉, Go루틴들은 OS 쓰레드와 1 대 1로 대응되지 않고, Multiplexing으로 훨씬 적은 OS 쓰레드를 사용한다.
> >
> >  메모리 측면에서도 OS 쓰레드가 1 메가바이트의 스택을 갖는 반면, goroutine은 이보다 훨씬 작은 몇 킬로바이트의 스택을 갖는다(필요시 동적으로 증가). Go 런타임은 Go루틴을 관리하면서 Go 채널을 통해 Go루틴 간의 통신을 쉽게 할 수 있도록 하였다.
> >
> > Thread는 16개의 범용 레지스터, Program Counter, Stack Pointer, Segment Register, 16 XMM registers, FP coprocessor state, 16 AVX registers, all MSRs etc를 스위칭
> >
> > Goroutine은 Program Counter, Stack Pointer, DX register
> >
> > [Register 참고](https://opentutorials.org/module/1087/7423)

```go
// helloWorld.go
package main
import (
    "fmt"
    "time"
)
func say(s string){
    println(s)
}
func main(){
    say("hell")
    go say("o")
    go say("wo")
    go say("rld")
    time.Sleep(time.Second * 3)
}
```

```bash
$ go run helloWorld.go
hell
wo
rld
o
```

실행 시점마다 다르게 출력

**익명함수 Goroutine**

```go
go func(s string){
    println(s) 
}("hello world")
```

**Goroutine sync**

```go
var wait sync.WaitGroup
wait.Add(개수)
go func(s string){
    defer wait.Done()
    println(s) 
}("hello world")
wait.Wait()
```

sync.WaitGroup을 이용하여 Wait()과 Done()을 이용하여 모든 goroutine 수행을 답보

**다중 CPU 처리**

```go
runtime.GOMAXPROCS(개수) //1: concurrent, 2: Parallel
```

개수는 Logical CPU 개수

**Concurrency**

> In programming, concurrency is the composition of independently executing processes, while parallelism is the simultaneous execution of (possibly related) computations. Concurrency is about dealing with lots of things at once. Parallelism is about doing lots of things at once.

## Go Channel

> 데이터를 주고받는 통로, 별도의 lock을 통한 대기 없이 데이터를 동기화 하는 기법
>
> 채널명 := make(chan 자료형)
>
> 채널명 <- 값 (송신)
>
> 변수명 <- 채널 (수신)

```go
package main
func main(){
    ch := make(chan int)
    go func(){
        ch <- 30405	// 송신
    }()
    var i int
    i = <- ch // 수신
    println(i)
}
```

Go channel은 수신자와 송신자가 서로를 기다리므로 다음과 같은 sync도 가능

```go

package main
import "fmt"
func main(){
    done := make(chan bool) // Unbuffered Channel
    go func(){
        for i:=0; i< 10; i++{
            fmt.Println(i)
        } 
        done <- true
    }()
    <-done
}
```

**Go channel buffering**

위와 같은 예제는 수신자가 데이터를 받을때 까지 송신자가 채널에 묶임(Deadlock)

channel에 값을 보내고 다른 일을 수행할 수 있도록 buffered channel 지원

```go
ch := make(chan int, 1)
ch <- 101
fmt.Println("hi")
```

**Channel parameter**

```go
func sendChan(ch chan <- string){}
func recvChan(ch <-chan string){}
```

화살표를 지정하여 송신채널, 수신채널을 구분하여 전달 가능

**Channel close**

```go
close(ch) // 송신은 불가능하지만 수신은 가능

for i:= range ch{
    println(i)
}

if _, success = <-ch; !success{
    println("ch is empty.")
}
```

**Channel select**

select를 이용하여 복수개의 channel의 데이터를 실행할 수 있다.

```go
package main
import "time"
func main(){
    done1:=make(chan bool)
    done2:=make(chan bool)
    
    go func(done chan bool){
        time.Sleep(1 * time.Second)
        done <- true
    }(done1)
    
    go func(done chan bool){
        time.Sleep(2 * time.Second)
        done <- true
    }(done2)
    
EXIT:
    for {
        select {
        case <- done1:
            println("done1 완료")
        case <- done2:
            println("done2 완료")
            break EXIT
        }
    }
}
```

