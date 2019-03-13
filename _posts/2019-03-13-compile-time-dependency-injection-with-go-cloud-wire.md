---
layout: post
comments: true
title: "Compile-time Dependency Injection with Go Cloud's Wire [번역]"
date: 2019-03-13 23:00:00 +0900
categories: back-end
description: golang의 의존성 주입 관련 프레임워크 공부와 번역을 통한 영어 공부
---

# Compile-time Dependency Injection with Go Cloud's Wire

> [The Go Blog - Compile-time Dependency Injection With Go Cloud's Wire (2018. 10. 9.)](https://blog.golang.org/wire) 번역; 영어공부 및 기술 공부

**The Go team recently announced the open source project**

Go 개발팀은 최근 Go Cloud라는 오픈소스를 공개했다.

**with portable Cloud APIs and tools for open cloud development**

[open cloud](https://cloud.google.com/open-cloud/) 개발을 위한 Cloud API와 도구를 함께

**This Post goes into more detail about Wire.**

이 포스트는 Wire에 대하여 더 자세하게 설명합니다.

**What problem does Wire solve?**

wire는 어떤 문제를 해결합니까?

**Depenendency Injection is a standard technique for producing flexible and loosely coupled code, by explicitly providing components with all of the dependencies they need to work.**

의존성 주입은 작동하는데 필요한 모든 의존성을 명시적으로 컴포넌트들에게 제공함으로써 유연하고 느슨하게 결합된 코드를 생성해주는 일반적인 기술입니다.

**In Go, this often takes the form of passing dependencies to constructors**

고 언어에서는 종종 의존성을 생성자에 전달하는 형태를 가집니다.

```go
// Config와 mysql.DB가 dependency이고 생성자 역할을 하는 함수의 파라미터에 전달하는 방식으로 의존성을 주입함
func NewUserStore(cfg *Config, db *mysql.DB) (*UserStore, error) {...}
```

> OOP의 위임자(Deligate) 패턴으로 불림
>
> A라는 클래스에 B라는 다른 클래스를 인스턴스로 가지고 비즈니스 로직을 B를 통해 구현하는 방식

**This technique works great at small scale, but larger applications can have a complex graph of dependencies, resulting in a big block of initialization code that's order-dependent but otherwise not very interesting.**

이 기술은 작은 규모에서 잘 동작합니다 그러나 보다 큰 어플리케이션들은 복잡한 의존성 그래프를 가질 수 있고, 결과적으로 순서에 의존하는 큰 블록의 초기화 코드가 생깁니다.

**It's often hard to break up this code cleanly, especially because some dependencies are used multiple times**

특히 일부 의존성들은 여러번 사용되기 때문에 자주 코드를 명확하게 해독하기 어렵게 합니다.

**Replacing one implementation of a service with another can be painful because it involves modifying the dependency graph by adding a whole new set of dependencies ( and their dependencies ...), and removing unused old ones.**

서비스의 한 구현체를 다른 것으로 대체하는 것은 고통스러울수 있습니다. 왜냐하면 그것은 완전히 새로운 의존성집합을 추가하거나, 사용하지 않는 오래된 것들을 지워서 의존성 그래프를 수정해야하기 때문입니다.

> 일반적으로 의존성 주입은 크게 세가지 형태로 사용할 수 있다.
>
> 생성자 주입, 세타 메소드 주입, 인터페이스 주입
>
> 세 가지 방법 모두 기본적으로 1 depth를 포함하며 중첩될 경우 복잡해 진다.
>
> 만약 주입하는 인스턴스의 내부에 pointer가 있다면 shallow copy가 발생할 것이며,
>
> 코드를 작성한 사람이 아닌 다른 사람이 그 부분을 잘못 수정을 하게 된다면 끔찍한 결과를 초래할 것이다.

**In practice, making changes to initialization code in applications with large dependency graphs is tedious and slow.**

실제로, 의존성 그래프가 큰 어플리케이션의 초기화코드를 변경하는 것은 지루하고 오래 걸립니다.

**Dependency injection tools like Wire aim to simplify the management of initialization code.**

 `Wire` 같은 의존성 주입 도구들은 초기화 코드 관리를 간단히 하는 것을 목표로 합니다.

**You describe your services and their dependencies, either as code or as configuration, then Wire processes the resulting graph to figure out ordering and how to pass each service what it needs.**

당신이 서비스 및 의존성을 코드 또는 설정으로 기술하면, 그 때 Wire는 그 결과 그래프를 처리하여 순서를 파악하고 각 서비스에 필요한 것들을 전달합니다.

**Make changes to an application's dependencies by changing a function signature or adding or removing an initializer, and then let Wire do the tedious work of generating initialization code for the entire dependency graph.**

함수 시그니처를 변경하거나 이니셜라이저를 추가하거나 제거하여 어플리케이션의 의존성을 변경한 다음 Wire가 전체 의존성 그래프에 대한 초기화 코드를 생성하는 지루한 작업을 수행하게 하십시오.

##  Why is this part of Go Cloud?

**Go Cloud's goal is to make it easier to write portable Cloud applications by providing idiomatic Go APIs for useful Cloud services.**

고 클라우드의 목표는 유능한 클라우드 서비스들을 위하여 제공되는 관용적인 Go API를 사용하여 이식성 있는 클라우드 어플리케이션을 작성하기 쉽게 하는 것입니다.

**For example, blob.Bucket provides a storage API with implementatinos for Amazon's S3 and Google Cloud Storage(GCS); applications written using blob.Bucket can swap implementations without changing their application logic.**

예를 들어 blob.Bucket은 아마존 A3와 구글 GCS를 위한 storage api를 제공합니다; blob.Bucket을 사용하여 작성된 어플리케이션들은 어플리케이션 로직을 수정하지 않고 구현체들을 교환할 수 있습니다. 

**However, the initialization code is inherently provider-specific, and each provider has a different set of dependencies.**

그러나, 초기화 코드는 기본적으로 제공자마다 다르며 각 제공자마다 다른 의존성 집합을 가지고 있습니다.

**For example, [constructing a GCS blob.Bucket](https://godoc.org/github.com/google/go-cloud/blob/gcsblob#OpenBucket) requires a gcp.HTTPClient, which eventually requires google.Credentials , while [constructing one for S3](https://godoc.org/github.com/google/go-cloud/blob/s3blob) requires an aws.Config, which eventually requires AWS credentials.**

예를 들어 GCS blob.Bucket 작성은 gap.HTTPClient가 필요하고, 결국 google.Crendential도 필요로 한다. S3를 작성하는 동안에는 aws.Configdhk AWS credentials를 필요로 한다.

