---
uuid: 2524
title: 如何用 OpenGL 封装一个 2D 引擎？
status: publish
categories: 图形编程
tags: 图形
date: 2016-08-11 01:51
slug: 
---

如何正确的使用 OpenGL “封装一个2D引擎” ？以下几个步骤：

1\. 别用什么 glBegin/glEnd，至少写兼容GLES2代码，不然手机上跑不起来。
2\. 用两个三角形的纹理拼凑出一个2D的图块出来，不是搞啥每个点自己画。
3\. 2D图像库基本就是要把显示对象树给做出来就得了。
4\. 每个显示对象除了自己外还有很多儿子节点。
5\. 每个显示对象有一个变换矩阵，用来设置位置和角度还有缩放，最后是节点的显示效果。
6\. 渲染的时候需要从远到近排序，并尽量归并相同效果（fs）及纹理。
7\. 把常用纹理管理起来，提供资源加载，可以换进换出，提供类 LRU的机制。
8\. 在此基础上提供一些动画（精灵）和场景控制的api，提供显示字体，即可。

最后推荐两个现成的轻量级2D引擎供阅读：

[StarEngine：GitHub - StarEngine/engine: Crossplatform C++11 2D Game Engine for Desktop and Mobile games](https://github.com/StarEngine/engine/)

[EJoy2D：GitHub - ejoy/ejoy2d: A 2D Graphics Engine for Mobile Game](https://github.com/ejoy/ejoy2d)

就是这样。

