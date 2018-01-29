---
layout: post
comments: true
title: "Android Custom Keyboard App 만들기"
date: 2018-01-29 22:55:00 +0900
categories: android
description: 두 번째 토이프로젝트 - 채키 \:최애 키보드
---

# Android Custom Keyboard App 만들기

## 두 번째 토이 프로젝트 채키: 최애 키보드

단톡방에서 채팅을 하다가 떠오른 아이디어

단톡방에서 보면 많은 사람들이 이모티콘과 사진등을 활용하는데 친구들 끼리 있는 방에서는 서로 엽기사진을 찍어놓고 공격하는 식의 채팅을 자주 볼 수 있다. 그러다가 좀더 쉽고 빠르게 사진을 보내고 싶다는 생각이 들었고 키보드에 커스텀을 하면 좋겠다는 생각을 했다.

기존의 채팅앱의 경우에는 아래와 같은 7단계를 거쳐야 사진을 전송할 수 있다.

```
1) + 버튼 누르기
2) 사진아이콘 누르기
3) 최근 사진의 리스트
4) 전체보기 버튼클릭
5) 상단 타이틀 바를 눌러서 앨범 선택하기
6) 사진 고르기
7) 전송하기
```

물론 즐겨찾기와 같은 기능들을 이용해서 상대방에게 사진을 전송 할 수 있겠지만

나는 좀 더 쉽고 빠르고 간편하게 사진을 전송할 수 있는 앱을 만들고 싶다.

## 시장 조사

먼저 만들기 전에 다른 사람들은 키보드앱을 어떻게 만들었는지 검색해봤다.

[알키보드](https://play.google.com/store/apps/details?id=com.estsoft.android.keyboard&hl=ko): 구글 스토어 키보드 검색 1등앱, 100만 이상 다운로드, 다양한 기능 제공

[Nota키보드](https://play.google.com/store/apps/details?id=com.notakeyboard&hl=ko): 오타방지 앱, 사용자의 입력 패턴 학습을 통한 오타 감소

[디자인 키보드](https://play.google.com/store/apps/details?id=com.designkeyboard.keyboard&hl=ko): 키보드 배경화면 사진, 테마, 움짤 등 다양한 기능 제공

오탈자, 배경, 테마, 저장된 이모티콘과 같이 거의 대부분 비슷비슷한 기능을 제공하는 키보드 뿐.. 내가 만들고자 하는 기능을 제공하는 앱은 아직 없는 것 같다. 

### 그렇다면 만들어서 써보자

## 오픈소스 및 자료 조사

1. [Let’s build a custom keyboard for Android](https://www.androidauthority.com/lets-build-custom-keyboard-android-832362/) : 커스텀 안드로이드 키보드 앱 만들기 블로그
2. [XhsEmoticonsKeyboard](https://github.com/w446108264/XhsEmoticonsKeyboard), [AwesomeKeyboard](https://github.com/RepoForks/AwesomeKeyboard) 키보드 오픈소스

## 목표

1. 키보드 설정
2. 앨범 만들기
3. 인물별 사진 앨범 자동 정리
4. 키워드 입력시 사진 자동 탐색
5. 모든 기능은 인터넷을 사용하지 않는 로컬 작업

## 개발 기간

2018.01.29. ~ 미정

10년 동안 유사한 앱이 없는 것을 보아 키보드 앱에서 사진에 접근하거나 외부 기능을 넣는 것에 제한이 있을지도 모르겠다는 생각이 든다 …. 제약이 많을 것 같은 느낌적인 느낌