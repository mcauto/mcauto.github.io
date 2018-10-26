---
layout: post
comments: true
title:  "Golang 문법 정리"
date:   2018-10-26 22:00:00 +0900
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

