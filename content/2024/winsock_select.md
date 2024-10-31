---
uuid: 3112
title: WinSock 的 select 如何超过 64 个套接字限制？（三种方法）
status: publish
categories: 网络编程
tags: 网络
slug: 
---
在做跨平台网络编程时，Windows 下面能够对应 epoll/kevent 这类 reactor 事件模型的 API 只有一个 select，但是却有数量限制，一次传入 select 的 socket 数量不能超过 FD_SETSIZE 个，而这个值是 64。

所以 java 里的 nio 的 select 在 windows 也有同样的数量限制，很多移植 Windows 的服务程序，用了 reactor 模型的大多有这样一个限制，让人觉得 Windows 下的服务程序性能很弱。

那么这个数量限制对开发一个高并发的服务器显然是不够的，我们是否有办法突破这个限制呢？而 cygwin 这类用 Win32 API 模拟 posix API 的系统，又是如何模拟不受限制的 poll 调用呢？

当然可以，大概有三个方法让你绕过 64 个套接字的限制。

#### 方法1：重定义 FD_SETSIZE

可以看 MSDN 中 winsock2 的 [select](https://learn.microsoft.com/en-us/windows/win32/api/winsock2/nf-winsock2-select) 帮助，这个 FD_SETSIZE 是可以自定义的：

> Four macros are defined in the header file Winsock2.h for manipulating and checking the descriptor sets. The variable FD_SETSIZE determines the maximum number of descriptors in a set. (The default value of FD_SETSIZE is 64, which can be modified by defining FD_SETSIZE to another value before including Winsock2.h.) 

而在 winsock2.h 中，可以看到这个值也是允许预先定义的：

```c
#ifndef FD_SETSIZE
#define FD_SETSIZE 64
#endif
```

只要你在 include 这个 winsock2.h 之前，自定义了 FD_SETSIZE，即可突破 64 的限制，比如在 cygwin 的 poll 实现 [poll.cc](https://github.com/Alexpux/Cygwin/blob/b61dc22adaf82114eee3edce91cc3433bcd27fe5/winsup/cygwin/poll.cc#L9)，开头就重定义了 FD_SETSIZE：

```c
#define FD_SETSIZE 16384		// lots of fds
#include "winsup.h"
#include <sys/poll.h>
#include <sys/param.h>
```

定义到了一个非常大的 16384，最多 16K 个套接字一起 select，然后 cygwin 后面继续用 select 来实现 posix 中 poll 函数的模拟。

