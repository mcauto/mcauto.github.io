---
layout: post
comments: true
title:  "React 시작하기"
date:   2019-02-15 23:08:00 +0900
categories: front-end
description: React 시작하기
---

# React 시작하기

Javascript 라이브러리 3대장 중 하나

사용자 인터페이스(User Interface; UI) 개발에 유용하다

모든 것은 컴포넌트다!

## 개발환경 구축하기

1. yarn 설치

yarn을 설치하고 react-app 프로젝트를 생성한다

```bash
$ brew install yarn
$ yarn create react-app deo-react
```

yarn을 설치하고 `yarn create react-app` 을 입력하여 프로젝트를 생성하면 프로젝트가 생성된다.

2. VSCode 설정하기 

VSCode plugin Prettier - code formatter를 설치하고 .vscode 디렉토리 하위에 settings.json에 다음 코드를 입력한다.

```json
{
	"eslint.autoFixOnSave": true,
	"editor.formatOnSave": true
}
```

위의 옵션은 javascript 코드를 작성하고 저장을 누르면 자동으로 코드 컨벤션으로 변경해준다. Golang에서 지원하는 gofmt와 흡사하다.

3. 생성된 react 앱을 이용하여 개발하기



## Javscript 유용한 문법

ES6 destructuring assignment

    const { name } = props;
    // const name = props.name;
    
    const MyName = ({ name }) => {
    	return (
    		<div>
    			{name} //props의 name만 꺼내온다.
    		</div>
    	);
    }

ES6 spread operator

    const object = { a: 1, b: 2, c: 3 };
    
    const nextObject = {
    	...object,
    	d: 4,
    	c: 10
    }
    console.log(nextObject)
    a: 1
    b: 2
    c: 10
    d: 4

​    
​    const objectArray = [
​        { id:1 },
​        { id:2 },
​    ];

ES6 computed property name

    var i = 0;
    var a = {
      ["foo" + ++i]: i,
      ["foo" + ++i]: i,
      ["foo" + ++i]: i
    };

ES6 template literal

    const hello = 'hello'
    const sentence = `안녕은 ${hello}`

ES6 array destructuring assignment

    const array = ['가', '나'];
    const[first, second] = array
    console.log(first) //가
    console.log(second) //나

ES6 Rest parameter

    function printAll(a, b, ...rest) {
    	console.log(a);
    	console.log(b);
    	console.log("----");
    	rest.forEach(i => console.log(i));
    }
    
    printAll(1,2,3,4,5,6,7,8);