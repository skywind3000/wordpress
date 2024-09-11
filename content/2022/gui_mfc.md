---
uuid: 2613
title: 用 MFC 写 GUI 程序是一种什么样的体验？
status: publish
categories: 编程技术
tags: GUI
slug: 
date: 2022-02-12 08:01
---
本文来自知乎问题：[MFC、WTL、WPF、wxWidgets、Qt、GTK 各有什么特点？](https://www.zhihu.com/question/23480014)

感觉我说了太多 Qt 的事情了，今天只说一下 MFC ，到底过时在哪里，都在说 "MFC 就是 xxx" 类似的话，我来补充点细节，增加点感性认识，到底 MFC 过时在哪里？想要用好 MFC 可以怎么办？

虽然 MFC 也有 DIALOG 的设计器，似乎可以拖一下控件，做个 hello world, 计算器之类的好像也很简单，但是稍微复杂那么一点就麻烦了，比如布局，MFC 里的控件只能设置绝对坐标和大小，那么如果你的窗口扩大或者缩小了，想自动改变内部特定控件的大小和位置怎么办？比如 C# 里随便设置一下各个控件的 docking 和 anchor 就能：

![](https://skywind3000.github.io/images/blog/2022/mfc_1.jpg)

> C# 里给控件设置 docking/anchor：窗口变大变小后就能自动调整控件的位置和大小

就能让某些控件随窗口变大而移动，某些控件随窗口变大而变大，而某些控件不变，这在任何 GUI 库里都是最基础的功能，都可以在设计器里点两下就做到的事情，MFC 却需要重载 WM_SIZE, WM_SIZING 消息来自己写代码每次手工计算所有控件的新坐标和大小，想写的通用点，还得上千行的代码，枚举所有子控件，根据额外信息重新计算位置大小，虽然 2015 的 MFC 里加了一个半成品的布局信息，但是基本没用，你在 MFC 的设计器里拖控件，都是写死坐标和大小的。（点击 Read more 展开）

<!--more-->

你也别说 c# 比 MFC 新，c# 的 docking 和 anchor 都是抄的 MFC 同期的 delphi 的布局方式，delphi 里叫做 align 和 anchors，c# 改都没改就换了个名字拿过去了。可以说布局是 GUI 库最基本的一个功能了，连 tkinter 都支持，MFC 却没有，而且持续十多年不思进取不增加。

再举个界面设计的常见操作，设置窗口的最小尺寸，其他编辑器里就是填写个窗口属性了事，MFC 里怎么做？要到 MainFrame 那里用 ClassWizard 找到 WM_GETMINMAXINFO 消息，为其生成一个函数，并编写：

```cpp
void CMainFrame::OnGetMinMaxInfo(MINMAXINFO* lpMMI) {
    CRect rc(0, 0, 400, 300);
    CalcWindowRect(rc);
    lpMMI->ptMinTrackSize.x = rc.Width();
    lpMMI->ptMinTrackSize.y = rc.Height();
}
```

是不是一脸懵逼？这 MINMAXINFO 是干嘛的？OnGetMinMaxInfo 到底什么时候被调用？CalcWindowRect 又是啥意思？看到这里你还想用么？

最后再举一个界面设计里最常见的例子，spliter bar，就是可以拖动改变左右两边控件/容器大小的分隔栏，比如资源管理器左边的文件树和右边的内容中间那根可以左右拖动控制改变左右两边控件尺寸比例的分隔栏就是 spliter bar，其他 GUI 库里就是设计器里拖出来点点点就创建好的东西，MFC 却不行，设计器里根本没有 spliter bar，需要在 OnCreateClient 函数里自己手工创建 CSplitterWnd，并且为左右两边分别创建两个 view，还要重载 WM_SIZE 消息，每次手工算位置，通知左右两个 view 更新大小，还有各种坑，其他 GUI 库一分钟做完的事情，你 MFC 里可能要搞一小时（算上编码和调试填坑时间）。

上面三个界面设计中最基础的概念：布局，控件细节配置（如最小尺寸），splitter bar，在 MFC 里都是空缺的，可以看出你想用它开发一个稍微复杂一点点的界面都是非常麻烦和琐碎的事情。

同期的 delphi/c++ builder 简直是甩 MFC 十条街，再一个是 MFC 的封装太浅了，基本就是 Win32 API 对 C++ 做了一层映射，加了一些宏而已，其他 GUI 库，包括 wxwidgets 你都不需要和 Win32 API 打交道，但你要写 MFC 不了解 Win32 API 是不可能的，比如 ClassWizard 里：

![](https://skywind3000.github.io/images/blog/2022/mfc_2.jpg)

你读不懂那一片 WM_ 的 Win32 消息是干嘛的，不了解 Win32 消息分发的机制，你基本别想写 MFC，而就算你用 wxWidgets 根本不需要去处理这么琐碎的事情，再一个是子控件管理，同期的界面库对窗口上的子控件都是直接封装成类的，并且按对象来组织。

MFC 里却和 Win32 程序一样，靠 ID 来管理，比如有一个静态文字 static text/label 之类的东西，你想改一下上面的字，MFC 里你先要找到这个 static text 的 id，然后用 ID 来获取类指针，然后再操作，比如：

```cpp
// TODO: Add your control notification handler code here
CStatic *st = (CStatic*)this->GetDlgItem(IDC_STATIC1);
st->SetWindowText(_T("hahahah"));
```

这基本就是 Win32 API 里的 GetDlgItem 和 SetWindowText：

![](https://skywind3000.github.io/images/blog/2022/mfc_3.jpg)

根据 ID 获取控件 HWND，只是把第一个参数给省略了。这个封装真的是 low 到家，围绕 ID 来组织控件这种 Win32 最原始的东西都要暴露出来，同期没有任何一个界面库需要直接操作控件 ID 的，不管同期的 Delphi 还是 wxWidgets 都是直接把每个子控件当作一个对象的，直接按对象来组织围绕对象开发即可。

封装太浅，很多东西又空缺，导致程序写大了一地碎鸡毛，还有人在多个窗口间靠 SendMessage 传指针来通信的，后期出点问题修都修不完。

那么 MFC 程序想写复杂了该怎么办呢？首先要靠编码规范来规避很多坑，比如多窗口间通信，就要约定只能纵向通信，拒绝横向通信，因为父亲控件控制子控件的生命周期，向下调用没问题，而子控件在生命周期内也有指向父控件的 parent 指针，那么上下级之间纵向通信是没问题的，父亲知道儿子什么时候被销毁，儿子也知道父亲永远在那里。但是要避免横向相互持有指针，那么兄弟控件通信可以绕道父节点或者 CMainFrame 那里去走一圈，避免直接兄弟之间直接指针调用方法，可以减少很多问题。

其次是自己要封装很厚的库，用来弥补 MFC 的不足，那么勉强一用，唯一的问题就是界面太丑了，不过有很多解决方案，比如用 skin++ 这类外挂库，两行代码，直接 hook 控件 redraw 的消息自己绘制：

![](https://skywind3000.github.io/images/blog/2022/mfc_4.jpg)

几行代码就可以换肤，这样对中型项目基本是足够了，想要做的更好点，基本就要自己绘制上 dui 了，中小团队很难玩得转，很多公司会选择购买一些成品的 dui 库结合 MFC 使用，比如迅雷的 bolt ，我当年一个项目买过 uipower 的 DirectUI 库，用了一段时间后还是被逼着走上了自己写 dui 的老路。

大部分成熟的 MFC 项目，到最后都会撸自己的 dui 代码，仅使用 MFC 一些基础功能，比如消息，CFrameWnd，CString 之类的，里面就是自己绘制，程序开头载入一个界面布局的 xml 文件，根据 xml 文件描述的内容载入对应资源自动生成 dui 的子控件，然后重新解释鼠标消息，对于像 TextEdit ，RichText 之类复杂的控件，还是会用 MFC 原有的封装一层盖上去，浮在你的 dui 界面上面。

最终费劲千辛万苦，你终于可以用 MFC 做一个类似 360 这样稍微丰富多彩点的消费级界面了：

![](https://skywind3000.github.io/images/blog/2022/mfc_5.jpg)

或者做出各种复杂度高的行业软件界面了，那么恭喜你，你在 MFC 里花了三年的时间，做出来的东西，终于摸到了只有半年经验的 Qt 程序员的脚后跟了。

