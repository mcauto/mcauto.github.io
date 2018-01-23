---
layout: post
comments: true
title:  "Android UI Open source 사용하기 "
date:   2018-01-23 23:50:00 +0900
categories: android
description: 안드로이드 UI 오픈소스 모음 repository인 awesome-android-ui 사용법
---

# Android UI Open source 사용

개인용 프로젝트를 할 때 UI까지 개발하는 것은 매우 힘들다

아이디어 구상이 끝나면 UI Open source를 사용하여 스토리보드를 만듦

 [awesome-android-ui](https://github.com/wasabeef/awesome-android-ui) 를 접속하면 Material 컴포넌트, Layout, Button, Menu, ViewPager 등 다양한 오픈소스 UI를 사용할 수 있다.

아래는 내가 주로 사용하는 오픈소스 리스트이다

```java
 // tabbar
    compile 'devlight.io:navigationtabbar:1.2.5'
    compile 'com.mikepenz:fontawesome-typeface:4.7.0.1@aar'
    compile 'com.github.apl-devs:appintro:v4.2.2'

    // Icon
    compile 'com.mikepenz:iconics-core:2.9.3@aar'

    // Icon Views
    compile 'com.mikepenz:iconics-views:2.9.3@aar'

    // fonts
    compile 'com.mikepenz:ionicons-typeface:2.0.1.3@aar'

    // binding
    compile 'com.jakewharton:butterknife:8.8.1'
    annotationProcessor 'com.jakewharton:butterknife-compiler:8.8.1'

    // dialog
    compile 'com.afollestad.material-dialogs:core:0.9.4.5'

    // permission
    compile 'gun0912.ted:tedpermission:1.0.3'

    // image selector
    compile 'com.github.nguyenhoanglam:ImagePicker:1.2.0'

    // json parser gson
    compile 'com.google.code.gson:gson:2.8.0'

    // YoYo animation
    compile 'com.daimajia.easing:library:2.0@aar'
    compile 'com.daimajia.androidanimations:library:2.2@aar'

    // image loader
    compile 'com.github.bumptech.glide:glide:4.3.1'
    annotationProcessor 'com.github.bumptech.glide:compiler:4.0.0'
    compile 'com.github.bumptech.glide:annotations:4.0.0-SNAPSHOT'
    compile 'jp.wasabeef:glide-transformations:3.0.1'

    // switchIcon
    compile 'com.github.zagum:Android-SwitchIcon:1.3.6'

    // custom font
    compile 'uk.co.chrisjenx:calligraphy:2.3.0'

    // searchToolbar
    compile 'com.github.udioshi85:libSearchToolbar:1.3.0'

    // license-fragment
    compile 'com.artit-k:license-fragment:1.3.0'

    // DB ORM
    compile 'org.greenrobot:greendao:3.2.2'

    // SQLCipher - DB Encryption
    compile 'net.zetetic:android-database-sqlcipher:3.5.7@aar'

    // TourGuide
    compile('com.github.worker8:tourguide:1.0.17-SNAPSHOT@aar') {
        transitive = true
    }

    // BigImageViewer
    compile 'com.github.piasy:GlideImageLoader:1.4.4'
    compile 'com.github.piasy:BigImageViewer:1.4.4'

    // swipeback
    compile project(':library')

    // appirater
    compile 'jp.co.recruit_mp:android-RMP-Appirater:1.1.1'
```

사용법은 각 오픈소스 repository를 따라 들어가면 상세히 설명이 되어있다.

대체적으로 gradle 파일에 compile 'open-source'를 입력하면 Android Studio에서 Sync하라는 알림이 뜬다.

build 버튼을 누르거나 sync를 누르면 자동적으로 다운로드 되며 프로젝트에서 import해서 사용할 수 있다.

각 Repository 마다 다르지만 오픈소스를 사용한 프로젝트가 링크되어있는 경우도 있으니 확인하면서 사용하면 되겠다.

오픈소스는 라이센스가 가장 중요한데 Github에 올라온 대부분의 오픈소스는 MIT, Apache와 같은 상업적인 용도도 가능한 라이브러리가 대부분이다.



## 참고 예시 

#### [챌범: 최고 애정 앨범](https://play.google.com/store/apps/details?id=com.gofd.mcauto.chaelbum)

개인용 잠금화면 안드로이드 앱 - 25개의 오픈소스 사용
