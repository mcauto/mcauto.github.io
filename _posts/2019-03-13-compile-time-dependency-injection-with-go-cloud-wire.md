---
layout: post
comments: true
title: "Compile-time Dependency Injection with Go Cloud's Wire [번역]"
date: 2019-03-14 23:00:00 +0900
categories: back-end
description: golang의 의존성 주입 관련 프레임워크 공부와 번역을 통한 영어 공부
---

# Compile-time Dependency Injection with Go Cloud's Wire

> [The Go Blog - Compile-time Dependency Injection With Go Cloud's Wire (2018. 10. 9.)](https://blog.golang.org/wire) 번역; 영어공부 및 기술 공부

**The Go team recently announced the open source project with portable Cloud APIs and tools for open cloud development**

[open cloud](https://cloud.google.com/open-cloud/) 개발을 위한 Cloud API와 도구를 함께 Go 개발팀은 최근 Go Cloud라는 오픈소스를 공개했다.

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

예를 들어 GCS blob.Bucket 생성은 gcp.HTTPClient가 필요하고 gcp.HTTPClient는 google.Crendential도 필요로 한다. S3를 작성하는 동안에는 aws.Config도 AWS credentials를 필요로 한다.

```go
//blob.Bucket을 반환하는 constructing function
func OpenBucket(ctx context.Context, client *gcp.HTTPClient, bucketName string, opts *Options) (*blob.Bucket, error)
// blob.Bucket을 위한 client constructing function
func NewHTTPClient(transport http.RoundTripper, ts TokenSource) (*HTTPClient, error)
// gcp.HTTPClient를 위한 TokenSourc constructing function
func CredentialsTokenSource(creds *google.Credentials) TokenSource
```

> 일반적으로 위와같이 하나의 인스턴스를 생성하기 위한 constructing function에 다른 의존성 인스턴스들이 있으면 계속해서 따라 들어가서 생성해주어야하는 노가다가 있다.

> 기존에 영어로 된 자료들을 검색하고 공부할 때는 공부가 된다고 생각했었다. 그러나 지금 직역하면서 공부를 해보니 공부가 안된 것 같다.

**Thus, updating an application to use a different blob.Bucket implementation involves exactly the kind of tedious update to the dependency graph that we described above.**

그러므로, 다른 blob.Bucket 구현체를 사용하기위해서 어플리케이션을 수정하는 것은 위에 서술한것과 같은 의존성 그래프를 수정하는 지루한 업데이트가 필요합니다.

**The driving use case for Wire is to make it easy to swap implementations of Go Cloud portable APIs, but it's also a general-purpose tool for dependency injection.**

Wire의 사용 사례는 Go Cloud portable API들의 구현체 변경을 쉽게해 주지만 의존성 주입을 위한 범용적 도구이기도 합니다.

>  Go cloud portable API를 사용할 때 편리하게 하려고 만들었지만 DI framework로도 충분히 사용할 수 있다는 것 같다.

## Hasn't this been done already?

> 이미 완료된것 아닙니까?

**There are a number of dependency injection frameworks out there.**

외부에 의존성주입 프레임워크들이 많이 있다.

**For Go, [Uber's dig](https://github.com/uber-go/dig) and [Facebook's inject](https://github.com/facebookgo/inject) both use reflection to do runtime dependency injection.**

고 언어를 위한 Uber의 dig와 facebook의 inject 둘 모두 런타임에 의존성 주입을 하기 위해 reflection을 사용합니다.

**Wire was primarily inspired by Java's [Dagger2](https://google.github.io/dagger/), and uses code generation rather reflection or [service locators](https://en.wikipedia.org/wiki/Service_locator_pattern).**

Wire은 주로 Java의 Dagger2에 영감을 받았습니다. 그리고 reflection 이나 service locators 대신 코드 생성을 사용합니다.

> Dagger2는 Google이 만들었다.

**We think this approach has several advantages:**

우리는 이 접근법이 다음과 같은 몇몇의 이점을 가지고 있다고 생각한다:

- **Runtime dependency injection can be hard to follow and debug when the dependency graph gets complex.**

  런타임 의존성 주입은 의존성 그래프가 복잡해지면 따라가기나 디버그 하기가 어려울 수 있다.

  **Using code generation means that the initialization code that's executed at runtime is regular, idiomatic Go code that's easy to understand and debug.**

  코드 생성을 사용한다는 것은 런타임에 실행되는 초기화 코드가 이해하거나 디버그하기 쉬운 규칙적이고 관용적인 고 언어 코드라는 것을 의미합니다.

  **Nothing is obfuscated by an intervening framework doing "magic".**

  마법을 부리는 중재 프레임워크에 의해 난독화 되는 것은 없다.

  **In particular, problems like forgetting a dependency become compile-time errors, not run-time errors.**

  특히, 의존성을 잃어버리는 것과 같은 문제들은 런타임 에러가 아니라 컴파일 시간 에러들이다.

- **Unlike [service locators](https://en.wikipedia.org/wiki/Service_locator_pattern), there's no need to make up arbitrary names or keys to register services.**

  서비스 로케이터들과는 달리 서비스를 등록하기 위해 임의의 이름이나 키를 작성할 필요가 없습니다.

  **Wire uses Go types to connect components with their dependencies.**

  Wire는 Go type을 사용하여 구성요소와 의존성을 연결합니다.

- **It's easier to avoid dependency bloat. Wire's generated code will only import the dependencies you need, so your binary won't have unused imports.**

  의존성을 부풀리는 것을 피하는 것은 쉽다. Wire의 생성 코드는 당신이 필요료하는 의존성들만 import될 것이다. 그리고 당신의 바이너리 파일은 사용하지 않는 import들은 가지고 있지 않을 것이다. 

- **Wire's dependency graph is knowable statically, which provides opportunities for tooling and visualization.**

  Wire의 의존성 그래프는 도구화 및 시각화를 위한 기회를 제공하는 것들로 static하게 알 수 있다.

## How does it work?

> 어떻게 동작하나요?

**Wire has two basic concepts: providers and injectors**

Wire는 두가지 기초 컨셉이 있다: providers와 injectors

**Providers are ordinary Go functions that "provide" values given their dependencies, which are described simply as parameters to the function.**

Provider는 단순히 함수에 대한 매개변수로 설명되는 종속성이 있을 경우 값을 제공하는 일반 Go 함수이다.

```go
// NewUserStore은 위에서 나온 함수와 같은 함수이다. 이 함수는 UserStore을 provide한다.
// *Config, *mysqlDB 종속성과 함께 제공한다.
func NewUserStore(cfg *Config, db *mysql.DB) (*UserStore, error){...}

// NewDefaultConfig는 *Config를 위한 Provider입니다.
func NewDefaultConfig() *Config{...}

// NewDB는 연결정보를 기초로하는 *mysql.DB를 위한 제공자입니다.
func NewDB(info *ConnectionInfo) (*mysql.DB, error){...}
```

**Providers that are commonly used together can be grouped into ProviderSets.**

일반적으로 함께 사용되는 공급자는 `ProvidersSets`으로 그룹화 할 수 있습니다.

**For example, it's common to use a defulat *Config when creating a *UserStore, so we can group NewUserStore and NewDefaultConfig in a ProviderSet:**

예를 들면, `*UserStore`를 생성할 때  default `*Config`를 사용하는 것이 일반적므로 우리는 `NewUserStore` 및 `NewDefaultConfig`를 `ProviderSet`에 그룹화 할 수 있습니다.

```go
var UserStoreSet = wire.ProviderSet(NewUserStore, NewDefaultConfig)
```

**Injectors are generated functions that call proviers in dependency order. You write the injector's signature, including any needed inputs as arguments , and insert a call to wire.Build with the list of providers or provider sets that are needed to construct the end result:**

Injector는 의존성 순서대로 호출되어 생성된 함수입니다. 당신이 injector의 signature를 작성하고 `wire.Build`의 최종 결과를 구성하는 데 필요한 Providers 또는 Provider 세트 목록을 삽입합니다.

```go
func initUserStore() (*UserStore, error){
    // 우리는 error를 얻을 것이다, NewDB는 *ConnectionInfo를 요구하기 때문이다.
    // 그리고 우리는 하나도 제공하지 않는다.
    wire.Build(UserStoreSet, NewDB)
    return nil, nil // 이 반환 값들은 무시된다.
}
```

**Now we run go generate to execute wire:**

지금부터 우리는 wire 실행을 통한 go generate를 실행합니다.

```bash
$ go generate
wire.go:2:10: inject initUserStore: no provider found for ConnectionInfo (required by provider of *mysql.DB)
wire: generate failed
```

**Oops! We didn't include a `ConnectionInfo` or tell Wire how to build one.**

이런! 우리는 ConnectionInfo 포함하지 않았으며, Wire에 빌드방법을 알려주지 않았습니다.

**Wire helpfully tells us the line number and types involved.**

Wire는 도움이 되도록 우리에게 줄번호와 타입을 알려줍니다.

**We can either add a provider for it to `wire.Build`, or add it as an argument:**

우리는 wire.Build에 provider를 추가하거나, 인수로 추가할 수 있습니다.

```go
func initUserStore(info ConnectionInfo) (*UserStore, error){
    wire.Build(UserStoreSet, NewDB)
    return nil, nil // 이 반환 값들은 무시된다.
}
```

**Now `go generate` will create a new file with the generated code:**

지금 go generate는 생성된 코드와 함께 새로운 파일을 생성할 것입니다.

```go
// File: wire_gen.go
// Code generated by Wire. DO NOT EDIT.
//go:generate wire
//+build !wireinject

func initUserStore(info ConnectionInfo) (*UserStore, error){
    defaultConfig := NewDefaultConfig()
    db, err := NewDB(info)
    if err != nil{
        return nil, err
    }
    userStore, err := NewUserStore(defaultConfig, db)
    if err != nil{
        return nil, err
    }
    return userStore, nil
}
```

**Any non-injector declarations are copied into the generated file.**

인젝터가 아닌 모든 선언들은 생성된 파일에 복사됩니다.

**There is no dependency on Wire at runtime: all of the written code is just normal Go code.**

런타임에 Wire에 대한 의존성은 없습니다. 모든 작성된 코드들은 단지 일반적인 Go 코드입니다.

**As you can see, the output is very close to what a developer would write themselves.**

보시다시피, output은 개발자가 직접 작성하는 것과 매우 비슷합니다.

**This was a trival example with just three components, so writing the initializer by hand wouldn't be too painful, but Wire saves a lot of manual toil for components and applications with more complex dependency graphs.**

이는 오직 세개의 컴포넌트들로 이루어진 단순한 예제 입니다. 손으로 initializer를 작성하는 것은 그렇게 고통스럽지 않지만 Wire는 복잡한 의존성 그래프들이 있는 구성요소와 응용프로그램에 많은 수고를 덜어 줍니다.

## How can I get involved and learn more?

> 어떻게 참여하고 더 많은 것을 배울수 있나요?

**The [Wire README](https://github.com/google/wire/blob/master/README.md) goes into more detail about how to use Wire and its more advanced features.**

Wire README에 Wire 사용방법과 더 많은 고급 기능을 사용하는 방법에 대해 자세하게 설명합니다.

**There's also a tutorial that walks through using Wire in a simple application**

또한 간단한 application에서 Wire를 사용하는 방법에 대한 튜토리얼도 있다.

**We appreciate any input you have about your experience with Wire!**

우리는 Wire에 대한 당신의 경험에 대한 의견을 보내주시면 감사하겠습니다.

**Wire's development is conducted on GitHub, so you can file an issue to tell us what could be better.**

Wire 개발은 Github에서 수행되므로 문제를 제기하여 개선점을 알려줄 수 있습니다.

**For updates and discussion about the project, join the Go Cloud mailing list.**

프로젝트에 대한 업데이트와 토론을 원하시면 Go Cloud mailing list에 가입하십시오.

**Thank you for taking the time to learn about Go Cloud's Wire.** 

Go Cloud의 Wire에 대하여 배우기 위해 시간을 내주어서 감사합니다.

**We're excited to work with you to make Go the language of choice for developers building portable cloud applications.**

Portable Cloud Application을 개발하는 개발자에게 적합한 언어를 선택하는 데 협조하게 되어 기쁘게 생각합니다.

**By Robert van Gent**

로버트 반 겐트