---
uuid: 2610
title: 给 Qt5 引入 C# / Delphi 的 Anchor Layout
status: publish
categories: 编程技术
tags: GUI
slug: 
date: 2022-02-16 02:04
---
在前文 [用 MFC 写 GUI 程序是一种什么样的体验？](/blog/archives/2613) 中提过 Anchor Layout 可以很简单的设定让控件跟随窗口四条边大小变化的策略：

![](https://skywind3000.github.io/images/blog/2022/qt_1.jpg)

比如右下角的两个按钮，设置的 anchor 是 "right,bottom" 他们在窗口扩大缩小时，会跟右和下两条边保持恒定距离，左上角的文字是 "left,top" 的 anchor，他会保持恒定的左边距和上边距，中间文字框的 anchor 是四个方向的 "left,top,right,bottom" 他会和窗口四条边框保持相同边距，因此会随窗口扩大而扩大。

这种布局方式最早是 Delphi / C++ Builder 引入的，非常简单实用，后来被 C# Winform 原封不动的抄了过去，而 QtWidgets 里用了另一套规则，虽然用起来更精细了，却没有 anchor layout 这么简单直白。

虽然 QtQuick 和 QGraphicsItem 里面也支持 anchor 布局，不过原生的 QtWidgets 里并没有支持，所以我写了两行代码解决了这个问题，只需要在窗体的 resizeEvent() 里调用下 AnchorLayout 类的 update() 方法，就能将所有子控件中包含 "anchor" 属性的 geometry 全部按照 c# 规则更新：(点击 Read more 展开)

<!--more-->

![](https://skywind3000.github.io/images/blog/2022/qt_2.jpg)

效果和 c# 一致，在设计器里也可以方便的添加 "anchor" 属性：

![](https://skywind3000.github.io/images/blog/2022/qt_3.png)

点击属性编辑器的 “+”按钮，添加一个名为 anchor 的字符串即可，主要去掉翻译：

![](https://skywind3000.github.io/images/blog/2022/qt_4.png)

就行了，不用的时候把该属性删除，或者填写 "left,top" ，空字符串在 anchor 布局中会让控件飘在空中，四处不挨。你基本可以像 c# 设计器那样在设计器里设置 anchor 了，顺便也支持了 dock 属性，看 demo 便知：

- https://github.com/skywind3000/toys/tree/master/Library/AnchorLayout

几处需要注意：

1) 很多 Qt 的控件在第一次被显示之前，大小是不确定的，因此需要像设计器一样提前精确 setGeometry，或者 show 以后再决定大小。
2) Anchor 布局中，对于容器控件，内部包含有相对坐标依赖的子控件时，需要提前先摆好位置，避免你初始化时的相对位置，在初次 update 后父控件的 geometry 变更，导致老的相对位置无法实用。

结束
