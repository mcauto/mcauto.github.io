---
layout: post
comments: true
title: "Android Seed Project 만들기 1"
date: 2018-01-24 23:39:00 +0900
categories: android
description: 빠른 안드로이드 앱을 만들기 위한 seed project
---

# Android Seed Project 만들기 1

## Why?

창업을 실패하고 운 좋게 좋은 회사에서 일을 하게 되었다.

앞으로의 시간 여유가 어떻게 될지 모르겠지만 한가할 때 하고자 했던 것들을 해보려고한다.

1. **1 Month, 1 App (1 Year 10 App): 올해 목표는 앱 10개 만들기 (프로젝트 포함)**
2. **1 Day, 1 Commit: 하루에 블로그 한번 커밋하기**

2년 동안 창업하면서 개발, 기획, 공모전 등을 하다보니 기록할 정신이 없었다. ~~핑계다~~

주말을 제외하고 1Day - 1Commit을 실천하다가 그냥 글만 기록하는 것 같아서 무슨 프로젝트를 할까 고민하다가

짧은 시간에 앱을 만들 수 있는 Seed App을 만들어야겠다고 생각했다.

개발을 하다보면 기능 개발보다 UI에 더 많은 시간이 소모되고, 창업을 하면서 사용자들이 많이 관심을 가지는 것은 기능보다는 UI라는 사실을 알게되었다. ~~당연하다.~~

이미 많은 seed 프로젝트가 있겠지만 내가 만든게 아닌 다른사람의 프로젝트는 구조 분석하는 것도 일이라 내가 직접 만들고자 한다.

## How?

일단은 내가 사용해본 오픈소스 위주로 개발할 예정이다.

[챌범: 최고 애정 앨범](https://play.google.com/apps/publish/?hl=ko&account=5107611040903352584)에 있는 개인용 앱에 필요한 오픈 소스부터 서버가 필요한 앱에 필요한 오픈소스까지 포스팅할 예정이다.

## When?

지금 바로 시작합니다.

## 안드로이드 UI 구성

먼저 앱을 처음 생성하면 액션 바와 Hello world라는 TextView를 볼 수 있는데 전부 다 지워준다.

TextView는 선택 후 Delete키를 눌러주면되지만 액션 바는 나중에 커스텀을 위해서 toolbar로 바꿔주어야 하므로 NoActionbar로 만들어야 한다. 

**기본 테마: NoActionBar**

#### values/styles.xml

```xml
<resources>
	<style name="AppTheme" parent="Theme.AppCompat.Light.NoActionBar">
        <item name="android:windowIsTranslucent">true</item>
        <item name="android:windowBackground">@android:color/transparent</item>
        <item name="android:windowNoTitle">true</item>
        <item name="windowActionBar">false</item>
        <item name="android:includeFontPadding">false</item>
        <item name="android:windowContentOverlay">@null</item>
    </style>
</resources>
```

**메인 액티비티: [NavigationTabBar](https://github.com/Devlight/NavigationTabBar), ViewPager, [Iconic](https://github.com/mikepenz/Android-Iconics)**

> NavigationTabBar를 사용하려면 [Butterknife](https://github.com/JakeWharton/butterknife)를 반드시 사용해야 함.

#### res/layout/activity_main.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#fff"
    android:orientation="vertical">
    <android.support.v4.view.ViewPager
        android:id="@+id/vp_horizontal_ntb"
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="1"/>

    <devlight.io.library.ntb.NavigationTabBar
        android:id="@+id/ntb_horizontal"
        android:layout_width="match_parent"
        android:layout_height="60dp"
        app:ntb_badge_gravity="top"
        app:ntb_badge_position="right"
        app:ntb_typeface="fonts/GodoM.ttf"
        app:ntb_bg_color="@android:color/white"
        app:ntb_badged="true"
        app:ntb_scaled="true"
        app:ntb_tinted="true"
        app:ntb_title_mode="all"
        app:ntb_titled="true"
        app:ntb_swiped="true"/>
</LinearLayout>
```

####build.gradle

```json
dependencies {
  // butterknife
  compile 'com.jakewharton:butterknife:8.8.1'
  annotationProcessor 'com.jakewharton:butterknife-compiler:8.8.1'
  //NavigationTabBar
  compile 'devlight.io:navigationtabbar:1.2.5'
  // Icon
  compile 'com.mikepenz:iconics-core:2.9.3@aar'
  // Icon-fonts
  compile 'com.mikepenz:ionicons-typeface:2.0.1.3@aar'
  compile 'com.mikepenz:fontawesome-typeface:4.7.0.1@aar'
}
```

설치방법은 위와같이 gradle에 추가하고 Sync를 누르면 된다.

#### MainActivity.java

```java
public class MainActivity extends AppCompatActivity {
    @BindView(R.id.ntb_horizontal)
    NavigationTabBar navTab;
    private ViewPager viewPager;
    private MainTabPagerAdapter viewPagerAdapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        ButterKnife.bind(this);
      	initUI();
    }

    private void initUI(){
        viewPager = findViewById(R.id.vp_horizontal_ntb);
        viewPagerAdapter = new MainTabPagerAdapter(getSupportFragmentManager());
        initPages();
        viewPager.setAdapter(viewPagerAdapter);
        initNavigationBar();
    }
    private void initPages() {
        viewPagerAdapter.addFragment(new Fragment());
        viewPagerAdapter.addFragment(new Fragment());
    }
    private void initNavigationBar(){

        int activeColor = getResources().getColor(R.color.tab_active);
        int inactiveColor = getResources().getColor(R.color.tab_inactive);

        navTab.setBgColor(Color.WHITE);
        navTab.setActiveColor(activeColor);
        navTab.setInactiveColor(inactiveColor);
        navTab.setIsTitled(true);

        final ArrayList<NavigationTabBar.Model> models = new ArrayList<>();

        Drawable iList = new IconicsDrawable(this, Ionicons.Icon.ion_ios_folder_outline).sizeDp(24);
		Drawable iCog =new IconicsDrawable(this).icon(FontAwesome.Icon.faw_cog).sizeDp(24);

        String modelBgColor = "#ffffff";
        models.add(
                new NavigationTabBar.Model.Builder(
                        iList,
                        Color.parseColor(modelBgColor))
                        .title(getString(R.string.main_nav_first))
                        .build()
        );
        models.add(
                new NavigationTabBar.Model.Builder(
                        iCog,
                        Color.parseColor(modelBgColor))
                        .title(getString(R.string.main_nav_second))
                        .build()
        );



        navTab.setModels(models);
        navTab.setViewPager(viewPager, 0);

        navTab.setBehaviorEnabled(true);
        navTab.setBadgeSize(20);

        navTab.setOnTabBarSelectedIndexListener(new NavigationTabBar.OnTabBarSelectedIndexListener() {
            @Override
            public void onStartTabSelected(final NavigationTabBar.Model model, final int index) {

            }

            @Override
            public void onEndTabSelected(final NavigationTabBar.Model model, final int index) {

            }
        });

        navTab.setOnPageChangeListener(new ViewPager.OnPageChangeListener() {
            @Override
            public void onPageScrolled(final int position, final float positionOffset, final int positionOffsetPixels) {

            }

            @Override
            public void onPageSelected(final int position) {

            }

            @Override
            public void onPageScrollStateChanged(final int state) {

            }
        });
        navTab.bringToFront();
    }
}
```

#### MainTabPagerAdapter.java

```java
public class MainTabPagerAdapter extends FragmentStatePagerAdapter {
    private List<Fragment> fragmentList = new ArrayList<>();

    public MainTabPagerAdapter(FragmentManager fragmentManager) {
        super(fragmentManager);
    }

    @Override
    public int getCount() {
        return fragmentList.size();
    }

    @Override
    public Fragment getItem(int position) {
        return fragmentList.get(position);
    }

    public void setFragmentList(List<Fragment> fragmentList) {
        this.fragmentList = fragmentList;
        notifyDataSetChanged();
    }
    public void addFragment(Fragment fragment) {
        fragmentList.add(fragment);
        notifyDataSetChanged();
    }

}
```

여기까지 주로 사용하는 앱의 네비게이션을 만들어보았다 안에 fragment를 사용하여 구성하면 된다.

다음편: ActionBar 커스텀, Fragment 사용하기



### 코드 확인 : [Android-seed-project](https://github.com/mcauto/Android-seed-project/tree/master)