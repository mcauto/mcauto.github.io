---
layout: post
comments: true
title: Coroutine과 Generator
date: 2018-10-16 23:00:00 +0900
categories: back-end
description: Python의 Coroutine과 Generator
---

# Coroutine

코루틴은 진입점이 여러개인 함수를 말한다. (표현이 난해하다고 생각한다. 같은 함수지만 호출 마다 return 값이 다르다? Function인데 Queue같다..?)

co-라는 접두어를 보면 알겠지만 병렬처리에 유용하다.

기존 multi threading 방식으로 개발을 하면 발생하는 문제점(Critical section 문제)들과 디버깅의 어려움이 존재하지만 coroutine을 이용하면 서로 다른 진입점에서 자기 할 일을 하고 끝을 낸다.

coroutine은 실행 시점에 다음 진입점을 넘긴다.

python에서는 tuple을  listcomp로 생성하면 generator를 반환한다.

```bash
>>> example = (i for i in range(5))
>>> example
<generator object <genexpr> at 0x104362938>
```

# Generator

generator는 iterator와 비슷하지만 다르다.

iterator는 반복자로서 iterable object를 read할 때 사용하는 객체지만,

generator는 호출 시점에 object를 반환하는 특별한 객체이다.

generator의 장점은 memory를 절약하는 효과를 볼 수 있다.

리스트는 memory에 데이터를 load한다.

리스트에 많은 양을 담아서 사용할 경우 한정된 memory 환경에서 문제를 야기한다.

그러나 generator는 사용시점에 메모리를 점유하는 방식으로 작동하므로 적은 메모리로도 많은 양을 컨트롤 할 수 있다.

물론 메모리가 충분히 크고 리스트의 사용이 매우 빈번할 경우에는 list가 generator보다 효율적이고 빠를 것이다.




