---
layout: post
comments: true
title:  "Android ORM GreenDAO 사용하기"
date:   2018-01-15 21:28:00 +0900
categories: android
description: 안드로이드 SQLite를 쉽게 사용하기 위한 ORM 오픈소스 사용법 
---

# Android ORM GreenDAO 사용하기

출처: [GreenDAO Github](https://github.com/greenrobot/greenDAO),  [GreenDAO document](http://greenrobot.org/greendao/documentation/updating-to-greendao-3-and-annotations/)

GreenDAO는 SQLite를 안드로이드에서 쉽게 쓸 수 있게 지원하는 오픈소스 라이브러리

## 설치하기 

Android Studio

1. build.gradle (Project: 앱이름) 파일

```java

buildscript {
    repositories {
        jcenter()
        mavenCentral() // 추가
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:2.3.3'
        classpath 'org.greenrobot:greendao-gradle-plugin:3.2.2' // 추가
    }
}
```

2. build.gradle(Module: app) 파일

```java
// build.gradle (Module: app) 제일 위에 입력
apply plugin: 'com.android.application'
apply plugin: 'org.greenrobot.greendao' // apply plugin
 
// 아래에 입력
dependencies {
    compile 'org.greenrobot:greendao:3.2.2' // add library
}
```

3. Sync Now 클릭 후 동기화 
4. 모델 만들기



```java
@Entity(nameInDb="posts")
public class Post{				// 객체 하나가 하나의 Row
  @Id(autoincrement = true)  	// AUTO_INCREASE
  private Long id; 				// id는 Long으로
  
  @Property(nameInDb="title")		// Column 이름
  private String title;
  
  @ToMany(referencedJoinProperty = "postId")	// 일대다 관계 Join
  @OrderBy("created ASC")						// 오름차순 정렬
  private List<Reply> replies;					// 댓글들 
}
```

5. Build (초록색 망치 Click)

```bash
# Build하면 아래의 경로에 greendao 객체 자동 생성
../프로젝트이름/app/build/generated/source/greendao

# 3개의 객체 생성
# PostDao.java				// Data Access Object
# DaoMaster.java
# DaoSession.java
```

6. Application 정의

```java
public class PostApplication extends Application{
  private DaoSession daoSession;
  public static final boolean ENCRYPTED = true;
  @Override
  public void onCreate(){
    super.OnCreate();
    DaoMaster.DevOpenHelper helper = new DaoMaster.DevOpenHelper(this, "db_name_encrypted" : "db_name");	// 데이터베이스 암호화
    Database db = ENCRYPTED ? helper.getEncryptedWritableDb("password") : helper.getWritable();
    daoSession = new DaoMaster(db).newSession();
  }
  public DaoSession getDaoSession(){return daoSession;}
}
```

7. Manifest 상속

```java
<application
	android:name=".PostApplication"
	....
```

8. Dao 사용하기 예제

```java
PostApplication postApp = (PostApplication) getApplication();
PostDao postDao = postApp.getDaoSession().getPostDao();
Long post_id = 1;
Post post = postDao.load(post_id);
post.setTitle("제목 바꾸기");
postDao.update(post);		// DB update

Post post = new Post();
post.setTitle("새로운 글");
postDao.insert(post);		// DB Insert
```

기본 함수: load(), insert(), update(), delete() 그 외 DB에서 데이터를 불러오는 다수의 함수 존재

9. Database 스키마가 변경 시: 스키마 버전 변경

```java
// build.gradle(Module: app)
greendao {
    schemaVersion 1 	// 반드시 현재보다 큰 숫자
}
```
#### 참고 예시

#### [챌범: 최고 애정 앨범](https://play.google.com/store/apps/details?id=com.gofd.mcauto.chaelbum)

개인용 잠금화면 안드로이드 앱
