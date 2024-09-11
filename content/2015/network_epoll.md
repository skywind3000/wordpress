---
uuid: 2521
title: EPoll 和高性能没什么关系
status: publish
categories: 网络编程
tags: Linux
slug: 
date: 2015-07-02 01:40
---
现在很多人一提高性能后端开发，就总会想起 EPoll 来。其实一个成熟的高性能服务器，epoll相关的代码，不到万分之一。

而往往入门服务端的人，都天真的人为：高性能服务端开发 == EPOLL，真好笑，之所以会出现 epoll这种被捧上天的垃圾，明明就是 posix 或者最早版本的 unix/bsd/systemv 的设计考虑不完善。

按今天的眼光反思 posix 和 unix/bsd/systemv 当年的设计，epoll 这种补丁就不应该实现。

异步 reactor 框架应该就只有一个简单而统一的 selector 就足够了，所有系统都相同，提供：

- register: 注册
- unregister：删除
- set：设置
- wait：等待事件
- read：读取事件
- wake：将等待中的 wait 无条件唤醒

别以为这些 poll / epoll / kevent / pollset / devpoll / select / rtsig
是些什么 “高性能服务器” 的 “关键技术”，它们只是一个 API，而且是对原有系统 API设计不完善打的补丁，各个内核实现了一套自己的补丁方式，它们的存在，见证了服务端技术碎片化的遗憾结果。

之所以会有这些乱七八糟的东西，就是早期的 posix / unix/ bsd /systemv 设计不周全，或者不作为留下的恶果。并非什么 “关键技术”。

不用提 windows 的 iocp了，proactor 会来强奸你代码结构，遭到大家唾弃是有原因的。不像 reactor那样优雅，所以 java nio 选择 reactor 是正确的。即便在 reactor 中，epoll 也是一个失败的例子，调用最频繁的 epoll_ctl 的系统占用估计大家都感受过吧，这方面 epoll 真该象 kevent / pollset 学习一下。

