---
uuid: 3112
title: WinSock 的 select 如何超过 64 个套接字限制？
status: publish
categories: 网络编程
tags: 网络
slug: 
---
在做跨平台网络编程时，Windows 下面能够对应 epoll/kevent 这类 reactor 事件模型的 API 只有一个 select，但是却有数量限制，一次传入 select 的 socket 数量不能超过 64 个：

```c
#ifndef FD_SETSIZE
#define FD_SETSIZE 64
#endif
```

所以 java 里的 nio 的 select 在 windows 也有同样的数量限制，那么我么是否有办法突破这个限制呢？而 cygwin 这类用 Win32 API 模拟 posix API 的系统，是如何模拟不受限制的 poll 调用呢？

当然可以，大概有两个方法让你绕过 64 个套接字的限制。

#### 方法1：重定义 FD_SETSIZE

可以看 MSDN 中 winsock2 的 [select](https://learn.microsoft.com/en-us/windows/win32/api/winsock2/nf-winsock2-select) 帮助：

> Four macros are defined in the header file Winsock2.h for manipulating and checking the descriptor sets. The variable FD_SETSIZE determines the maximum number of descriptors in a set. (The default value of FD_SETSIZE is 64, which can be modified by defining FD_SETSIZE to another value before including Winsock2.h.) 


