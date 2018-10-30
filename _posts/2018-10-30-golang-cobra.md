---
layout: post
comments: true
title:  "Cobra를 이용한 Go Cli 프로그램 만들기"
date:   2018-10-30 22:00:00 +0900
categories: back-end
description: docker에도 사용된 cli 개발 모듈 cobra를 사용하여 프로그램을 만들어보자
---

# Cobra를 이용한 Go Cli 프로그램 만들기

참고: [cobra github](https://github.com/spf13/cobra)

>cobra: Go cli module 
>
>CLI : Command Line Interface

cobra는 docker 프로젝트에서 사용된 cli 모듈로 빠르게 프로젝트를 개발할 수 있다.

물론, go에서는 cli를 위한 기본 패키지 flag도 있다.

하지만 cobra generator를 사용하면 매우 빠르고 쉽게 cli 프로그램을 개발 할 수 있다.

## 설치하기

단순히 go get으로 모듈을 설치하여 import 방식으로 사용해도 좋지만

cobra generator를 이용하면 더 간단하게 만들 수 있으므로 다음과 같이 설치

```bash
$ go get -u github.com/spf13/cobra/cobra
```

설치 후 다음과 같이 `cobra` 를 입력하면 cobra를 cli로 사용할 수 있다.

```bash
$ cobra
Cobra is a CLI library for Go that empowers applications.
This application is a tool to generate the needed files
to quickly create a Cobra application.

Usage:
  cobra [command]

Available Commands:
  add         Add a command to a Cobra Application
  help        Help about any command
  init        Initialize a Cobra Application

Flags:
  -a, --author string    author name for copyright attribution (default "YOUR NAME")
      --config string    config file (default is $HOME/.cobra.yaml)
  -h, --help             help for cobra
  -l, --license string   name of license for the project
      --viper            use Viper for configuration (default true)

Use "cobra [command] --help" for more information about a command.
```

## 개발하기

```bash
$ mkdir cobra-example
$ cd cobra-example
$ cobra init
Your Cobra application is ready at
/Users/mcauto/go/src/cobra-example

Give it a try by going there and running `go run main.go`.
Add commands to it by running `cobra add [cmdname]`.
$ ls
LICENSE cmd     main.go
$ tree cmd
cmd
└── root.go

0 directories, 1 file
```

먼저 프로젝트 디렉토리를 만들고 `cobra init` 명령어를 통해 cli 프로젝트의 틀을 만들 수 있다.

`cobra add` 명령어를 사용하여 프로그램의 command를 추가할 수 있다.

```bash
$ cobra add version
version created at $GOPATH/src/cobra-example/cmd/version.go
$ go run main.go
A longer description that spans multiple lines and likely contains
examples and usage of using your application. For example:

Cobra is a CLI library for Go that empowers applications.
This application is a tool to generate the needed files
to quickly create a Cobra application.

Usage:
  cobra-example [command]

Available Commands:
  help        Help about any command
  version     A brief description of your command

Flags:
      --config string   config file (default is $HOME/.cobra-example.yaml)
  -h, --help            help for cobra-example
  -t, --toggle          Help message for toggle

Use "cobra-example [command] --help" for more information about a command.
$ go run main.go version
version called
```

간단히 version이라는 명령어를 추가해보았다.

cmd 디렉토리 하위에 version.go 파일이 자동으로 생겼다.

코드를 간단하게 살펴보자

```go
// Copyright © 2018 NAME HERE <EMAIL ADDRESS>
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

// versionCmd represents the version command
var versionCmd = &cobra.Command{
	Use:   "version",
	Short: "A brief description of your command",
	Long: `A longer description that spans multiple lines and likely contains examples
and usage of using your command. For example:

Cobra is a CLI library for Go that empowers applications.
This application is a tool to generate the needed files
to quickly create a Cobra application.`,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("version called")
	},
}

func init() {
	rootCmd.AddCommand(versionCmd)

	// Here you will define your flags and configuration settings.

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	// versionCmd.PersistentFlags().String("foo", "", "A help for foo")

	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	// versionCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}

```

Use, Short, Long, Run이 cobra 모듈의 Command 구조체의 필드이다.

영어를 보면 알겠지만 Use는 호출 명령어 이름, Short는 짧은 설명, Long은 긴 설명이다.

여기서 가장 중요한건 Run 필드이다.

프로젝트에 추가한 version command를 사용하면 호출되는 함수라는 것을 쉽게 알 수 있다.

## 배포하기

Go 언어로 작성한 프로그램의 배포는 매우 간단하다.

main 패키지가 존재하는 디렉토리에서 `go build` 명령어만 입력하면 프로젝트명의 실행파일이 생성된다.

그리고 그 바이너리 파일을 실행시키면 끝

주의할 점은 go는 오래된 운영체제에서 돌아가지 않는다.

자세한 requirements는 [여기](https://golang.org/doc/install#requirements)에서 확인

