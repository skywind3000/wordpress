---
uuid: 3039
title: 桌面开发用 Tkinter/wxPython/PyQt 哪个好？
status: publish
categories: 编程技术
tags: GUI,Python
slug: 
date: 2022-01-15 14:42 
---
Python 有很多 GUI 框架，比如著名的 Tkinter，wxPython 和 PyQt，那么想用 Python 开发桌面软件的话选哪个更好呢？作为三个都用过的人先给个结论，不用纠结，直接选 PyQt 即可。

很多人说 Tkinter 简单无依赖，没错，但这就是 tkinter 唯一的仅存的优点了，但是请大家注意，Tkinter 的这个 "简单"，是指 "功能少和效果单一”，不是写程序简单明了，真正写起程序来还是 PyQt 最简单清晰。

有些东西你学出来就过时了，比如 “算盘”，比如 Tkinter 和 wxPython；而有的东西你学会了，即便不吃这碗饭，不靠它涨工资，也能在今后一二十年持续受益，比如练习打字速度，比如背单词，比如学习 PyQt。

对于桌面开发，天下武功那么多，PyQt 既是最正统的门派，同时又是一系列综合技术的组合，它近可以同 C++ Qt 无缝整合，解决性能相关的东西；退，又有基于 chromium 的 QtWebEngine ，能在适合跑页面的部分用 html/js 来写页面，并和 python 双向调用，实现类似 cef/Electron 的效果，但是 Electron 这类单一解决方案就只能用 web 技术，想反过来同 native 界面混合开发，基本就傻了，碰到性能问题又不能像 PyQt 那样可以无缝切换 C++ Qt，所以庞然大物 Electron 只适合呆在自己的舒适区。

往左，QtWidgets 可以和传统 C# 的 WinForm pk，往右，Qt-Quick 可以同 WPF/XAML 看齐，因此你可以把 PyQt/Qt 看成一系列界面解决方案的 “超集”，所以学习 PyQt 你学会的是综合格斗术，是名门正派的内功心法，而不是某方向单一的方案，比如 “螳螂拳”。

PyQt 就是一扇门，它通往的是最专业的桌面解决方案的世界。

看了不少挺 Tkinter 的，他们用 Tkinter 用的都太浅了，知乎上有个最高赞用 Tkinter 费力拙略地模仿了个背单词的 anki，也许他不知道，他所模仿的 anki 其实本身就是用 PyQt 开发的。

真的用的深的只有这个回答：
[为何很多Python开发者写GUI不用Tkinter，而要选择PyQt和wxPython或其他？](https://www.zhihu.com/question/32703639/answer/170291468)

我曾经用 Tkinter 做过一些内部工具，比如给线上网络服务做的一个 RPC 调试终端：

![](https://skywind3000.github.io/images/blog/2022/qt/q1.jpg)

当时我就是图别的同事使用时不用装其他库，结果写到后面，越做越后悔。

（点击 continue/more 继续）

<!--more-->

最开始碰到的问题是 Tkinter 作为一个标准 GUI 库，里面没有 ComboBox，你们信吗？就是上图中间那个下拉选单，最基础的控件了，翻遍文档没有，最后在扩展库 ttk 里面才找到，所以千万别被简单所迷惑，tk 的简单是缺胳膊丢大腿的简单，是 “不完整”。

其次是状态栏，很多资料只教你画窗体上的控件，对状态栏语焉不详，或者只教你创建，不教你更新，不教你窗口尺寸改变的时候怎么去改变状态栏上各段的大小。

还有个大问题是文档奇缺，碰到问题到处搜，到处都找不到，某些小众论坛里找到只言片语，你就求神拜佛了，比如布局上面，上面窗口如果扩大了，我想下面控制面板部分只有最左边的输入框会跟随扩大，右边的一系列控件保持不变，就这个简单的布局，官方文档语焉不详，网上信息支离破碎，我搞了三天才搞定，你们信不信？

其次就是天花板低，上面这个简单的小工具基本就是顶着 Tkinter 的上限做的：

机制简陋，大量主要操作全靠字符串传递，比如改变大小，PyQt 是：

```python
widget.setGeometry(100, 100, 640, 480)
```

而 Tkinter 是：

```python
root.geometry("%dx%d+%d+%d"%(width, height, x, y))
```

上面两段代码，哪段更简单清晰？哪段更一目了然？

这就是我对 Tkinter 最初的感觉：flaky，太简陋，Tkinter 里一大半操作都是字符串操作，比如禁止某个控件（让输入框无法输入，按钮无法按），用 PyQt 写起来很清晰：

```python
widget.setDisabled(True)
widget.setDisabled(False)
```

换成 Tkinter 的话，是：

```python
widget.config(state = 'disabled')
widget.config(state = 'normal')
```

我就问问，上面下面的两种代码风格，你想写哪一种？我喜欢 PyQt 这种明白无误的，因为正常编辑器 / IDE 都有补全，我写完 widget 后面写一个句号，自动补全就能把这个控件能做什么，全部给我列的清清楚楚，而字符串操作，你基本就蒙圈了。

我之前还以为 Tkinter 禁止控件 "disable" 后再恢复用 "enable" ，结果调试半天，没用，最后又找了很多文档，发现应该是用 "normal" 字符串，这不是坑人么？做同样的事情，Tkinter 写起来需要更多的查文档，关键是它文档还特别缺。

Tkinter 不但写起来需要查很多文档，读起来也含糊很多，需要花更多时间去理解，不像 PyQt 那样清晰明白，所以 Tkinter 的 "简单" 是指 "功能少" 和 “简陋”，并不是指开发起来比 PyQt 简单，基本上 Tkinter 程序写大点就容易乱，不好维护。

#### DirectUI

做桌面的都知道，每个操作系统都提供了一系列标准控件，按钮，输入框之类的，直接用就是写出那种最古坂的界面来，虽然可以重定义颜色，自定义 OnPaint 之类的绘制函数，但是限制是非常大的：

- 性能不高，每个按钮，Label 都是一个操作系统的 HWND 资源，控件多了性能不行。
- 各个操作系统标准控件不同，功能也不同，做跨平台依靠这些标准组件，就只砍功能作飞线。
- 灵活度太差了。
  
所以成品桌面软件，不管你们看到的 360/迅雷/QQ，都使用自己绘制自己做事件响应的方式，称为 DirectUI，只有最外层的大窗口用操作系统提供的标准组件，里面都是自己管理的，因此又称为 Windowless 的开发方式。

其中 Tkinter/wxPython 都是用的标准组件，同时他们为了跨平台保持一致性，还会舍弃很多平台独有的功能，而只有 Qt 是从最底层就使用 DirectUI 自己绘制的机制来实现界面的。

你要做商业项目，界面稍微 fancy 一点，你只有一条路，就是 DirectUI，一般大厂的 DirectUI 库基本都是自己撸的，国内有一套 duilib，以前还卖钱，现在好像开源了，但是还是用的 GDI 来绘制，只支持 Windows，而 Qt 的绘制系统是直接硬件加速的。

开发 dui 系统非常复杂，以前我碰到别人写的一个四万行的 edit 控件，偶尔出现一个问题，20-30 层的 C++ 调用栈，找都没处找，它不是一般公司一般团队玩得转的，但是现在用 PyQt，你个人几行代码就能站在巨人的肩上瞬间实现最高级最正宗的界面系统。

#### 事件机制

比如我曾经想给 TextEdit 控件加个按 CTRL+回车 的事件，Tkinter 里就只有一个 bind 接口：

```python
edit.bind('<Control-Enter>', self.on_hotkey_ctrl_enter)
```

没错，又是字符串问题，这里不提有多坑了，关键是这个机制问题，Tkinter 为了捕获键盘专门做了一个 bind，而 Qt 提供的是更灵活的消息重载、消息 filter 机制，让你可以处理所有消息，不当是键盘消息，同时还可以决定消息的流向，是否拦截。

PyQt 里还有 QAction 机制，可以让多个功能相同的控件（比如菜单里的保存，和工具条上的保存按钮）都指向一个相同的 QAction，再由这个 QAction 来绑定代码里的函数。而 Tkinter 或者 wxpython 里没有这个机制，你只能为这些事件绑定代码。

PyQt 的信号机制可以串联，可以将按钮的 clicked 信号直接连接到其他按钮的 click 槽上，或者连接到窗口的 close 上面，不用写代码 designer 里拖动一下就能设置很多关联事件。

#### 界面风格

上面也说了，由于 Tkinter 和 wxpython 都是用操作系统提供的控件，因此风格很难改变，Tkinter 最丑，因为它只能改颜色，wxpython 好歹还提供了一个 OnPaint 事件，让你自己绘制，这样好歹可以做的稍微多样化一点，但是也和之前直接用 MFC 的 OnPaint 绘制界面一样，性能差，走的 GDI，界面稍微一复杂点，resize 一下就卡了。

OnPaint 还有一个问题是你只能做规则形状的控件，所有控件都必须是规则的矩形，想花哨点都没法，因为每次 OnPaint 进来就是让你绘制一个矩形区间，虽然可以用半透明模拟，但是性能太差了，最后代码和界面耦合度太高，全部搅在一起，换风格就要改代码。

那么 PyQt 使用 DirectUI 的机制获取了最大灵活度以后，它是如何解决的呢？PyQt 有从低到高各个层次的解决方法，其中最多的就是 QSS，一套类似 CSS 的机制，让风格设计可以完全交给设计师，同时换风格也不用改代码：

![](https://skywind3000.github.io/images/blog/2022/qt/q2.jpg)

大概是这样，并且 PyQt 内置了好几套默认风格，你要切换只需要简单的一句：

```python
window.changeStyle("windows")
```

你就得到一个 windows xp 风格的界面：

![](https://skywind3000.github.io/images/blog/2022/qt/q3.jpg)

看起来和 Tkinter 一样丑？没事，继续：

```python
window.changeStyle("windowsvista")
```

立马变身 vista 风格：

![](https://skywind3000.github.io/images/blog/2022/qt/q4.jpg)

还有更现代一点的 “Fusion”风格：

![](https://skywind3000.github.io/images/blog/2022/qt/q5.jpg)

不高兴你还可以把默认风格导出来，用 qss 编辑器修改微调，然后另存成别的风格。

#### 联动 Web

商用桌面软件，一般主体界面，主要面板用 Qt/PyQt 开发，而对于一些经常变动的，比如活动抽奖页面之类的，排行榜之类天天变来变去，方便远程更新的，用 Web 页面更方便。

PyQt 4.x 的时候还在用 Webkit，到了 5.x 以后已经升级为更现代的基于 Chromium 的 QtWebEngine，你可以理解成一个小型的 cef/electron 了。

Python 可以通过 QWebChannel 注册一个函数给 javascript 调用，Python 也可以用 eval 来执行某个 javascript 函数，还可以共享各种数据，这样 js 可以专注页面，然后用 Python 来实现 native 功能。

#### 学习成本

从头学起 Tkinter 一点不比 PyQt 简单，PyQt 接口更加清晰和现代，Tkinter 接口再众多 GUI 体系中可以用 “老旧”和 "古怪”，不像 PyQt 那么符合直觉，因此 Tkinter 写同样的功能要查更多的文档，最后，文档还十分稀缺。

另外是你花了很多时间学会了 Tkinter，突然有一天，你会碰到一个小需求，比如布局中窗口拉伸时想指定各个控件的拉伸比例，比如想给 combobox 里加个图片，你搜尽网上所有 Tkinter 的文档，你才发现 Tkinter 完全做不了，这样的事情一次两次以后，你就非常容易后悔当初选择了 Tkinter 了，因为同样的时间，你早学会 PyQt 两遍了。

三个界面比较方案，Tkinter 的天花板只有三层楼那么高，wxPython 有十层楼，而 PyQt 的天花板，上不封顶，它没有天花板。

因此既然学习成本类似，说实话 Tkinter 学习成本略高，wx 和 PyQt 类似，当然选择天花板最高的东西学。

#### 混合开发

PyQt 可以无缝同 C++ Qt 整合，大部分界面可以用 PyQt 直接实现，少部分影响性能的地方，比如单独某个复杂窗口，或者带有特殊功能并且要显示几万行数据的 treeview，表格等，可以用 C++ 来实现，导出给 PyQt 调用。

要性能 C++ Qt 可以秒杀任何 Electron/C# 的解决方案，更别说 tk/wx 了。要开发便捷，PyQt 本身就是可以快速堆功能，快速出效果的解决方案。

论扩展能力，网上还有大量的 Qt 的开源控件，比如 Markdown Preview，比如 QScintilla（用来方便显示源代码语法高亮的控件，类似 QTextEdit），PyQt 都可以直接拿过来用。Tkinter 和 wx 这方面真的很惨白。

#### 为什么我没用 wxpython ？

一句话就是我碰到 wxpython 的天花板了，说实话，wxpython 也能构造复杂的界面，当初我用 wxpython 给一款即时通信软件做过界面，然后，当我想要定制样式，由于缺乏 DirectUI 机制的灵活性，我只能在非常有限的条条框框下定义。

其实我的定制也没感用多复杂，就是给这个控件加个背景，给那个控件实现个 OnPaint 方法，然后当我试着拖动改变窗口大小，它卡了。

我以前用 MFC、C++ Builder 下面自己接管 OnPaint 的时候都很流畅啊，但为啥 wxpython 它就卡了呢？是不是我哪里没有用对？然后我研究了两个星期，试尽了所有方式，看完了相关的所有文档，性能有所提升，但是没有本质改善。

最后我终于意识到，我又碰到 wxpython 的天花板了。

#### 哪些项目用 PyQt 开发的？

Eric Python IDE:

![](https://skywind3000.github.io/images/blog/2022/qt/q6.png)

音乐编辑软件：Frescobaldi

![](https://skywind3000.github.io/images/blog/2022/qt/q7.png)

比如著名的科学计算 IDE：Spyder

![](https://skywind3000.github.io/images/blog/2022/qt/q8.png)

数据挖掘系统 Orange：

![](https://skywind3000.github.io/images/blog/2022/qt/q9.jpg)

什么叫专业桌面软件？上面这些就是。还有很多其他使用 PyQt 的项目：

- 浏览器（支持 vim 键位操作的）：qutebrowser
- 网盘：DropBox
- 背单词软件：Anki
- 电子书制作：Calibre

#### 我是怎么开始用 PyQt 的？

我是走了很多弯路，最终才选择了 PyQt 的，曾经被 wxpython/c# 的性能坑过，被 MFC/DirectUI 的复杂性和出 BUG 很难找的问题折磨过。

我当时是想要解决团队使用 C++ dui 开发时 bug 查证太耗时间的问题，需求变动越来越频繁，但是 C++ dui 开发逐渐快 hold 不住了。

这时我看到了 Qt/PyQt 的解决方案，一开始还是很谨慎的，我让几个应届生新人尝试用 PyQt 做一点简单功能，统计下来，15个应届生，在刚刚学会 Python 以后，平均两周的时间就能学会 PyQt，然后再用两周的时间可以用 PyQt 写一个类似 winamp 的界面比较 fancy 的音乐播放器，还支持 overlay 动态显示歌词。

于是我开始有了一点信心，逐渐在正式的项目里逐渐引入 PyQt 来做一些新功能，然后通过对比发现，应届生开发了两个月 PyQt 以后，他们的开发效率，相当于一个五年工作经验的 C++ MFC 程序员，不论是出活的速度，还是代码稳定性。

得到这个结论以后，启动了客户端产品的 Qt/PyQt 重构工作，也没花多长时间，把老的 MFC/Dui 方案全部换成了 Qt+PyQt 的解决方案，又花了点时间稳定上线后，整个产品迭代速度问题和稳定性问题才终于得到解决。

那些 5+ 年工作经验的 MFC 程序员一旦从 MFC/dui 的泥塘里解放出来，也很快能够投入并适应 C++ Qt 的开发节奏，他们主要做一些复杂的界面和高性能的东西，平时负责优化和裁剪 Qt 库。

同时对于很多变化频繁的东西，当使用 PyQt 4 的 Webkit 来跑 js 页面。

保守估计，半年过后，整个 20+ 人桌面团队的开发效率，比之前翻了 2-3 倍。

#### 为什么推荐 PyQt ?

上手容易，天花板高，它并不比 tkinter/wxpython 难学，写起代码来也较前两者更为简单清晰，代码易读性和可维护性都比前两个强。前两者就像学打算盘，你学出来你就落伍了，而 PyQt 学会了，你可以在十年二十年内持续受益。

关键，PyQt 有海量的学习资料，比如这本《PyQt5快速开发与实战》就不错：

只要走过弯路，被其他 GUI 系统坑过，并真的在正式产品里使用过 PyQt 你就会发现，投入学习 PyQt 的时间是完全值得的，这玩意儿学了你不吃亏，学了你不上当。

你不一定会从事专业桌面开发，但小到做点个人小玩具，给组内做点工具什么的，大到开发正式产品，同 C++ Qt 结合，它的天花板永远比你的需求要高。

--

PS：纠结 PyQt 是 GPL 授权的可以用 PySide，LGPL 协议，一样的接口，随意闭源商业发布。

很多人问 PyQt 如何打包？我手工打包 PyQt5 只有 14MB：
[怎么样打包 pyqt 应用才是最佳方案？](https://skywind.me/blog/archives/3002)

根本无需 PyInstaller 。


--

相关阅读：
[用 MFC 写 GUI 程序是一种什么样的体验？](https://skywind.me/blog/archives/2613)

