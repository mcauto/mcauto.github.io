---
layout: post
comments: true
title: "Android Seed Project 만들기 3"
date: 2018-06-17 21:50:00 +0900
categories: android
description: 빠른 안드로이드 앱을 만들기 위한 seed project3
---

# Android Seed Project 만들기 3

[1편](https://mcauto.github.io/android/2018/01/24/android-seed-project/)에서는 기본 메인 액티비티에 [NavigationTabBar](https://github.com/Devlight/NavigationTabBar)을 추가하고 [Iconic](https://github.com/mikepenz/Android-Iconics)을 이용해 아이콘도 추가하였다.

[2편](https://mcauto.github.io/android/2018/01/25/android-seed-project2/)에서는 앱의 타이틀바(혹은 액션바) 커스텀과 Fragment를 이용해 페이지를 만들어 보았다.

3편에서는 Kotlin으로 코드를 수정하여 보았다. Android Studio 3.0부터는 자동변환 기능이 있지만 그저 단순변환이므로 코틀린을 학습하면서 조금씩 코드 구조도 다듬었다.

기존의 프로젝트에서 브랜치만 분리하여 kotlin으로 작성하였다.

**master branch = 자바**

**kotlin branch = 코틀린**

## 코틀린 개발 방법

**코틀린 사용**

1. build.gradle(Module:app) 파일의 최상단 kotlin-android plugin 추가
2. build.gradle(Project:Android-seed-project)에 kotlin_version, classpath 추가
3. dependencies에 kotlin-stdlib 추가

**kotlin android extensions 사용**

1. `import kotlinx.android.synthetic.activity_main.*` 을 추가 
2. activity_main.xml의 View id들을 변수처럼 사용

**build.gradle(Application:Android-seed-project)**

```bash
// Top-level build file where you can add configuration options common to all sub-projects/modules.

buildscript {
    ext.kotlin_version = '1.2.30' # 추가
    repositories {
        google()
        jcenter()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:3.1.3'
        classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:$kotlin_version" # 추가

        // NOTE: Do not place your application dependencies here; they belong
        // in the individual module build.gradle files
    }
}

allprojects {
    repositories {
        google()
        jcenter()
    }
}

task clean(type: Delete) {
    delete rootProject.buildDir
}

```

**Build.gradle(Module:app)**

```bash
apply plugin: 'com.android.application'

apply plugin: 'kotlin-android' #추가
apply plugin: 'kotlin-android-extensions' #추가

dependencies {
	...
    implementation "org.jetbrains.kotlin:kotlin-stdlib:$kotlin_version" #추가
    implementation "org.jetbrains.kotlin:kotlin-stdlib-jre7:$kotlin_version" #추가
}

```



## 언어별 코드 비교

**MainActivity.java**

```java
public class MainActivity extends AppCompatActivity {
  @BindView(R.id.ntb_horizontal)
  NavigationTabBar navTab;
  private ViewPager viewPager;
  private MainTabPagerAdapter viewPagerAdapter;

  @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate (savedInstanceState);
    setContentView (R.layout.activity_main);
    ButterKnife.bind (this);
    initUI ();
  }

  private void initUI() {
    viewPager = findViewById (R.id.vp_horizontal_ntb);
    viewPagerAdapter = new MainTabPagerAdapter (getSupportFragmentManager ());
    initPages ();
    viewPager.setAdapter (viewPagerAdapter);
    initNavigationBar ();
  }

  private void initPages() {
    viewPagerAdapter.addFragment (SampleFragment.newInstance ());
    viewPagerAdapter.addFragment (new Fragment ());
  }

  private void initNavigationBar() {

    int activeColor = getResources ().getColor (R.color.tab_active);
    int inactiveColor = getResources ().getColor (R.color.tab_inactive);

    navTab.setBgColor (Color.WHITE);
    navTab.setActiveColor (activeColor);
    navTab.setInactiveColor (inactiveColor);
    navTab.setIsTitled (true);

    final ArrayList<NavigationTabBar.Model> models = new ArrayList<> ();

    Drawable iList = new IconicsDrawable (this, Ionicons.Icon.ion_ios_folder_outline).sizeDp (24);
    Drawable iCog = new IconicsDrawable (this).icon (FontAwesome.Icon.faw_cog).sizeDp (24);
    String modelBgColor = "#ffffff";
    models.add (
            new NavigationTabBar.Model.Builder (
                    iList,
                    Color.parseColor (modelBgColor))
                    .title (getString (R.string.main_nav_first))
                    .build ()
    );
    models.add (
            new NavigationTabBar.Model.Builder (
                    iCog,
                    Color.parseColor (modelBgColor))
                    .title (getString (R.string.main_nav_second))
                    .build ()
    );


    navTab.setModels (models);
    navTab.setViewPager (viewPager, 0);

    navTab.setBehaviorEnabled (true);
    navTab.setBadgeSize (20);

    navTab.bringToFront ();
  }
}
```

**MainActivity.kt**

```kotlin
class MainActivity : AppCompatActivity() {
  private lateinit var viewPagerAdapter: MainTabPagerAdapter

  override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    setContentView(R.layout.activity_main)
    initUI()
  }

  private fun initUI() {
    initPages()
    initNavigationBar()
  }

  private fun initPages() {
    viewPagerAdapter = MainTabPagerAdapter(supportFragmentManager)
    viewPagerAdapter.addFragment(SampleFragment().newInstance())
    viewPagerAdapter.addFragment(Fragment())
    viewPager.adapter = viewPagerAdapter
  }

  private fun initNavigationBar() {
    val activeColor = resources.getColor(R.color.tab_active)
    val inactiveColor = resources.getColor(R.color.tab_inactive)
    navTab.bgColor = Color.WHITE
    navTab.activeColor = activeColor
    navTab.inactiveColor = inactiveColor
    navTab.setIsTitled(true)

    navTab.models = initNavTabs()
    navTab.setViewPager(viewPager)
    navTab.isBehaviorEnabled = true
    navTab.badgeSize = 20f
    navTab.bringToFront()
  }

  private fun initNavTabs(): ArrayList<NavigationTabBar.Model> {
    val tabs: ArrayList<NavigationTabBar.Model> = ArrayList()
    val listIcon: Drawable = IconicsDrawable(this, Ionicons.Icon.ion_ios_folder_outline).sizeDp(24)
    val settingIcon: Drawable = IconicsDrawable(this).icon(FontAwesome.Icon.faw_cog).sizeDp(24)
    val listTitle = getString(R.string.main_nav_first)
    val cogTitle = getString(R.string.main_nav_second)
    val listTab = Builder(listIcon, Color.WHITE).title(listTitle).build()
    val settingTab = Builder(settingIcon, Color.WHITE).title(cogTitle).build()

    tabs.add(listTab)
    tabs.add(settingTab)

    return tabs
  }
}
```

**MainTabPagerAdapter.java**

```java
public class MainTabPagerAdapter extends FragmentStatePagerAdapter {
  private List<Fragment> fragmentList = new ArrayList<> ();

  public MainTabPagerAdapter(FragmentManager fragmentManager) {
    super (fragmentManager);
  }

  @Override
  public int getCount() {
    return fragmentList.size ();
  }

  @Override
  public Fragment getItem(int position) {
    return fragmentList.get (position);
  }

  public void setFragmentList(List<Fragment> fragmentList) {
    this.fragmentList = fragmentList;
    notifyDataSetChanged ();
  }

  public void addFragment(Fragment fragment) {
    fragmentList.add (fragment);
    notifyDataSetChanged ();
  }
}
```

**MainTabPagerAdapter.kt**

```kotlin
class MainTabPagerAdapter(fragmentManager: FragmentManager) : FragmentStatePagerAdapter(fragmentManager) {
  private var fragmentList: MutableList<Fragment> = ArrayList()

  override fun getCount(): Int {
    return fragmentList.size
  }

  override fun getItem(position: Int): Fragment {
    return fragmentList[position]
  }

  fun setFragmentList(fragmentList: MutableList<Fragment>) {
    this.fragmentList = fragmentList
    notifyDataSetChanged()
  }

  fun addFragment(fragment: Fragment) {
    fragmentList.add(fragment)
    notifyDataSetChanged()
  }
}
```

**SampleFragment.java**

```java
public class SampleFragment extends Fragment {
  public SampleFragment() {  }

  public static SampleFragment newInstance() {
    return new SampleFragment ();
  }

  @Nullable
  @Override
  public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
    View view = inflater.inflate (R.layout.fragment_sample, container, false);
    initToolbar (view);
    return view;
  }

  private void initToolbar(View view) {
    if(Build.VERSION.SDK_INT >= 21) {
      // 21 버전 이상일 때
      getActivity ().getWindow ().setStatusBarColor (Color.BLACK);
    }
    Toolbar toolbar = view.findViewById (R.id.toolbar);
    toolbar.setTitle ("");

    ((AppCompatActivity) getActivity ()).setSupportActionBar (toolbar);

    TextView title = toolbar.findViewById (R.id.title);
    title.setText ("main");
  }
}
```

**SampleFragment.kt**

```kotlin
class SampleFragment : Fragment() {
  fun newInstance(): SampleFragment {
    return SampleFragment()
  }

  override fun onCreateView(inflater: LayoutInflater?, container: ViewGroup?, savedInstanceState: Bundle?): View? {
    val view = inflater!!.inflate(R.layout.fragment_sample, container, false)
    if (Build.VERSION.SDK_INT >= 21)
      activity.window.statusBarColor = Color.BLACK
    view.toolbar.title.text = "hi"
    activity.setActionBar(toolbar as Toolbar?)
    return view
  }
}
```

# 코틀린 사용 후기

단순하게 기존에 만든 프로젝트를 코틀린으로 변경하는 작업이라 크게 사용한 기술은 없었지만

사용하면서 되게 코딩이 편하다는 느낌을 받을 수 있었다. ~~기술보다는 IDE가 사기 같다. 갓텔리제이 만세~~ 

가장 좋았던 장점은 getActivity(), findViewById() 등의 함수없이도 바인딩이 된다는 점이 좋았다.

**Kotlin Android Extensions** 이라고 부르며 xml에 있는 View들의 id를 변수로 사용할 수 있는 점이 좋았다.



### 코드 확인 : [Android-seed-project](https://github.com/mcauto/Android-seed-project/tree/master)