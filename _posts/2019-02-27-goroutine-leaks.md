---
layout: post
comments: true
title:  "고루틴 누수 - 유기된 리시버"
date:   2019-02-27 23:22:00 +0900
categories: back-end
description: 종료되지 않는 고루틴의 메모리 누수 번역
---

# Goroutine Leaks - The Abandoned Receivers([출처](https://www.ardanlabs.com/blog/2018/12/goroutine-leaks-the-abandoned-receivers.html))

### Introduction

고루틴 누수는 Go 프로그램의 메모리 누수의 일반적인 원인입니다. 이전 글에서 goroutine 누수의 소개와 많은 Go 개발자가 실수하는 일반적인 예제를 소개했습니다. 이어서 이번 글에서는 고루틴 누수가 발생할 수 있는 다른 시나리오를 소개하겠습니다.

### Leak: 유기된 리시버(The Abandoned Receivers)

이 누수 예제 프로그램에서는 절대 보내지 않을 값을 받기위해 여러 고루틴들이 block된 것을 볼 수 있습니다. 예제 프로그램은 하나의 파일을 사용하여 record batch 처리를 하기위해 여러 고루틴을 시작합니다. 고루틴은 하나의 인풋 채널으로 부터 각각 값을 받고 새로운 값들을 아웃풋 채널을 통하여 보냅니다.

### Example

[실행 링크](https://play.golang.org/p/Jtpla_UvrmN)

**code**

```golang
package main

import (
	"fmt"
	"runtime"
	"strings"
	"time"
)

func main() {
	// 시작 시점의 고루틴 개수 저장
	startingGs := runtime.NumGoroutine()

	names := []string{"Anna", "Jacob", "Kell", "Carter", "Rory"}
	processRecords(names)
	
	// processRecords의 내부에서 고루틴으로 호출된 worker 함수의 수행을 기다림
	time.Sleep(time.Second) 

	// 종료 시점의 고루틴 개수 저장
	endingGs := runtime.NumGoroutine()

	// Report the results.
	fmt.Println("========================================")
	fmt.Println("Number of goroutines before:", startingGs)
	fmt.Println("Number of goroutines after :", endingGs)
	fmt.Println("Number of goroutines leaked:", endingGs-startingGs)
}

// 작업을 수행하는 함수
func processRecords(records []string) {
	total := len(records)
	input := make(chan string, total)
	for _, record := range records {
		input <- record
	}
	// input 채널을 닫지 않을 경우 goroutine leak이 발생
	// close(input) 

	output := make(chan string, total)
	// CPU 개수만큼 workers 개수 저장
	workers := runtime.NumCPU()
	for i := 0; i < workers; i++ {
		// 이 부분에서 memory leak 발생
		go worker(i, input, output) 
	}
	for i := 0; i < total; i++ {
		result := <-output
		fmt.Printf("[result  ]: output %s\n", result)
	}
}

func worker(id int, input <-chan string, output chan<- string) {
	// input채널은 buffered channel이므로 buffer 크기만큼 무한 대기
	for v := range input {
		fmt.Printf("[worker %d]: input %s\n", id, v)
		output <- strings.ToUpper(v)
	}
	fmt.Printf("[worker %d]: shutting down\n", id)
}
```

**output**

```bash
$ go run main.go
[worker 7]: input Anna
[worker 3]: input Jacob
[result  ]: output ANNA
[result  ]: output JACOB
[worker 7]: input Carter
[worker 1]: input Kell
[worker 5]: input Rory
[result  ]: output CARTER
[result  ]: output KELL
[result  ]: output RORY
========================================
Number of goroutines before: 1
Number of goroutines after : 9
Number of goroutines leaked: 8
```

코드 관련 설명을 하나하나 하는 것보다 전체적으로 코드를 보여주는 것이 나을 것 같아서 통으로 들고 왔습니다.

위의 예제는 goroutine 내부의 buffered 채널(input)으로 인한 무한 대기 현상으로 발생하는 goroutine leak 케이스입니다.

Buffered channel은 채널에 buffer 크기를 정하여 channel의 값을 받는 곳에서 buffer 크기만큼 기다리게 되어있습니다. 

buffered 채널의 특징은 다음과 같습니다.

1. buffer 사이즈 만큼 channel에 전달되면 대기
2. 채널의 수신자가 없어도 보낼 수 있음
3. range를 이용하여 채널이 닫힐 때까지 수신

하지만 위의 코드를 보면 input 채널을 닫지 않는다면 채널이 닫힐 때 까지 range문에서 channel을 수신합니다. 따라서 고루틴은 영원히 종료되지 않습니다. 만약 특정 시간마다 names를 파일에서 읽어와서 go routine을 생성한다면 메모리는 계속해서 증가하게되고 결국 OOM이 발생하여 프로세스는 종료될 것입니다.

### Fix: Signal Completion

주석 처리된 input의 close함수를 이용하여 채널을 닫아주면 worker 내부의 input의 반복문을 빠져나오면서 worker 함수가 종료된다.

### Conclusion

golang의 goroutine을 이용한 동시성 개발을 할 때는 [반드시 goroutine이 종료되도록 개발해야 한다](https://dave.cheney.net/2016/12/22/never-start-a-goroutine-without-knowing-how-it-will-stop). 그렇지 않으면 goroutine leak이 쌓여 OOM(Out of memory)가 발생할 것이고 프로그램은 의도치 않게 종료될 것이다.

***동시성은 매우 유용한 도구입니다, 그러나 그것은 반드시 주의해서 사용해야합니다.***

사실 블로그의 글을 훑어보고 초반부는 번역하다가 나중에는 혼자 보기 편하게 수정해서 정리했습니다.

goroutine이 경량쓰레드로 다른 언어에서의 쓰레드보다 비용이 적게 들지만([참고](https://tech.ssut.me/goroutine-vs-threads/)) 메모리 제한이나, 데몬과 같은 프로그램을 만들 때는 확실하게 이해하고 사용해야 한다.

채널은 고루틴을 가장 쉽게 사용할 수 있게 도와주지만 수신 채널과 송신 채널을 구분하지 않으면 스파게티 요리사가 될 수 있다.