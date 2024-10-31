---
uuid: 3112
title: WinSock 的 select 如何超过 64 个套接字限制？（三种方法）
status: publish
categories: 网络编程
tags: 网络
slug: 
---
在做跨平台网络编程时，Windows 下面能够对应 epoll/kevent 这类 reactor 事件模型的 API 只有一个 select，但是却有数量限制，一次传入 select 的 socket 数量不能超过 `FD_SETSIZE` 个，而这个值是 64。

所以 java 里的 nio 的 select 在 Windows 也有同样的数量限制，很多移植 Windows 的服务程序，用了 reactor 模型的大多有这样一个限制，让人觉得 Windows 下的服务程序性能很弱。

那么这个数量限制对开发一个高并发的服务器显然是不够的，我们是否有办法突破这个限制呢？而 cygwin 这类用 Win32 API 模拟 posix API 的系统，又是如何模拟不受限制的 poll 调用呢？

当然可以，大概有三个方法让你绕过 64 个套接字的限制。

#### 方法1：重定义 FD_SETSIZE

首先可以看 MSDN 中 winsock2 的 [select](https://learn.microsoft.com/en-us/windows/win32/api/winsock2/nf-winsock2-select) 帮助，这个 `FD_SETSIZE` 是可以自定义的：

> Four macros are defined in the header file Winsock2.h for manipulating and checking the descriptor sets. The variable FD_SETSIZE determines the maximum number of descriptors in a set. (The default value of FD_SETSIZE is 64, which can be modified by defining FD_SETSIZE to another value before including Winsock2.h.) 

而在 `winsock2.h` 中，可以看到这个值也是允许预先定义的：

```c
#ifndef FD_SETSIZE
#define FD_SETSIZE 64
#endif
```

只要你在 include 这个 `winsock2.h` 之前，自定义了 `FD_SETSIZE`，即可突破 64 的限制，比如在 cygwin 的 poll 实现 [poll.cc](https://github.com/Alexpux/Cygwin/blob/b61dc22adaf82114eee3edce91cc3433bcd27fe5/winsup/cygwin/poll.cc#L9)，开头就重定义了 `FD_SETSIZE`：

```c
#define FD_SETSIZE 16384		// lots of fds
#include "winsup.h"
#include <sys/poll.h>
#include <sys/param.h>
```

定义到了一个非常大的 16384，最多 16K 个套接字一起 select，然后 cygwin 后面继续用 select 来实现 posix 中 poll 函数的模拟。

这个方法问题不大，但有两个限制，第一是到底该定义多大的 `FD_SETSIZE` 呢？定义大了废内存，每次 select 临时分配又一地内存碎片，定义少了又不够用；其次是程序不够 portable，头文件哪天忘记了换下顺序，或者代码拷贝到其它地方就没法运行。

因此我们有了更通用的方法2。

（点击 more/continue 继续）

<!--more-->

#### 方法2：自定义 fd_set 结构体

这个方法更为通用，按照 MSDN 里的 [fd_set](https://learn.microsoft.com/en-us/windows/win32/api/winsock2/ns-winsock2-fd_set) 定义：

```cpp
typedef struct fd_set {
  u_int  fd_count;
  SOCKET fd_array[FD_SETSIZE];
} fd_set, FD_SET, *PFD_SET, *LPFD_SET;
```

结构体里第一个成员 `fd_count` 代表这个 `fd_set` 里总共保存了多少个套接字，而后面的 `fd_array` 数组则存储了各个套接字的值，它的大小由前面的 `FD_SETSIZE` 宏决定，这决定了最大可存储数量。

我们来看看 `winsock2.h` 中几个操作 `fd_set` 的宏的实现：

```cpp
#ifndef FD_ZERO
#define FD_ZERO(set) (((fd_set *)(set))->fd_count=0)
#endif
```

清空操作很简单，就是把 `fd_count` 设置成零就行了，而增加一个套接字：

```cpp
#define FD_SET(fd, set) do { u_int __i;\
    for (__i = 0; __i < ((fd_set *)(set))->fd_count ; __i++) {\
        if (((fd_set *)(set))->fd_array[__i] == (fd)) {\
            break;\
        }\
    }\
    if (__i == ((fd_set *)(set))->fd_count) {\
        if (((fd_set *)(set))->fd_count < FD_SETSIZE) {\
            ((fd_set *)(set))->fd_array[__i] = (fd);\
            ((fd_set *)(set))->fd_count++;\
        }\
    }\
    } while(0)
```

简单来讲就是先判断数组里是否已经包含，如果没包含并且 `fd_count` 小于 `FD_SETSIZE` 的话就追加到 `fd_array` 后面并且增加 `fd_count` 值。

那么方案就是用一个动态结构模拟这个 `fd_set` 就行了，要用时直接强制类型转换成 `fd_set` 指针传递给 `select` 即可，微软的 devblogs 里一篇文章讲过这个方法：

- [A history of the fd_set, FD_SETSIZE, and how it relates to WinSock](https://devblogs.microsoft.com/oldnewthing/20221102-00/?p=107343)

但是它的实现是用模板做了个新的 `fd_set` 结构体，一旦实例化就定死了，我给一个更好的跨平台实现：

```cpp
#define ISOCK_ERECV		1		/* event - recv           */
#define ISOCK_ESEND		2		/* event - send           */
#define ISOCK_ERROR		4		/* event - error          */

/* iselect: fds(fd set), events(mask), revents(received events) */
int iselect(const int *fds, const int *events, int *revents, 
    int count, long millisec, void *workmem);
```

这个函数第一个参数 `fds` 传入 fd 数组，然后 `events` 传入对应 fd 需要捕获的事件，相当于 poll 里的 events，而 `revents` 用于接受返回的事件，最后 `count` 代表总共有多少个 fd，前面的参数模仿了 poll 函数只是没用 `struct pollfd` 这个结构体表达而已。

最后一个参数 `workmem` 代表需要用多少内存，如果为 `NULL` 的话，这个函数不会调用下层的 select/poll 而会根据 `count` 数量计算出需要用到的内存并返回给你，让你安排好内存，第二次调用时用 `workmem` 传入内存指针：

```cpp
int my_select1(const int *fds, const int *event, int *revent, int count, long millisec) {
    int require = iselect(NULL, NULL, NULL, count, 0, NULL);
    if (require > current_buffer_size) {
        current_buffer = realloc(current_buffer, require);
        current_buffer_size = require;
    }
    return iselect(fds, event, revent, count, millisec, current_buffer);
}
```

这样用就行了，这个 `current_buffer` 可以是一个全局变量，也可以放在你封装的 selector/poller 对象里。

或者栈上开辟一块空间，如果少量 select 就用栈空间，否则临时分配：

```cpp
int my_select2(const int *fds, const int *event, int *revent, int count, long millisec) {
    #define MAX_BUFFER_SIZE 2048
    char *stack[MAX_BUFFER_SIZE];
    char *buffer = stack;
    int require = iselect(NULL, NULL, NULL, count, 0, NULL);
    if (require > MAX_BUFFER_SIZE) buffer = (char*)malloc(require);
    int hr = iselect(fds, event, revent, count, millisec, buffer);
    if (buffer != stack) free(buffer);
    return hr;
}
```

这样可以避免维护一个全局变量。

下面给出 `iselect` 这个函数的实现，它能完全模拟 poll 的行为，突破 `FD_SETSIZE` 的限制，并且在非 Windows 下用 poll 而 Windows 下用 select：

```cpp
/* iselect: fds(fd set), events(mask), revents(received events) */
int iselect(const int *fds, const int *events, int *revents, int count, 
    long millisec, void *workmem)
{
    int retval = 0;
    int i;

    if (workmem == NULL) {
        #if defined(__unix) || defined(__linux)
        return count * sizeof(struct pollfd);
        #else
        size_t unit = (size_t)(&(((FD_SET*)0)->fd_array[1]));
        size_t size = count * sizeof(SOCKET) + unit + 8;
        return (int)(size * 3);
        #endif
    }    
    else {
        #if defined(__unix) || defined(__linux)
        struct pollfd *pfds = (struct pollfd*)workmem;

        for (i = 0; i < count; i++) {
            pfds[i].fd = fds[i];
            pfds[i].events = 0;
            pfds[i].revents = 0;
            if (events[i] & ISOCK_ERECV) pfds[i].events |= POLLIN;
            if (events[i] & ISOCK_ESEND) pfds[i].events |= POLLOUT;
            if (events[i] & ISOCK_ERROR) pfds[i].events |= POLLERR;
        }

        poll(pfds, count, millisec);

        for (i = 0; i < count; i++) {
            int event = events[i];
            int pevent = pfds[i].revents;
            int revent = 0;
            if ((event & ISOCK_ERECV) && (pevent & POLLIN)) 
                revent |= ISOCK_ERECV;
            if ((event & ISOCK_ESEND) && (pevent & POLLOUT))
                revent |= ISOCK_ESEND;
            if ((event & ISOCK_ERROR) && (pevent & POLLERR))
                revent |= ISOCK_ERROR;
            revents[i] = revent & event;
            if (revents[i]) retval++;
        }

        #else
        struct timeval tmx = { 0, 0 };
        size_t unit = (size_t)(&(((FD_SET*)0)->fd_array[1]));
        size_t size = count * sizeof(SOCKET) + unit + 8;
        FD_SET *fdr = (FD_SET*)(((char*)workmem) + 0);
        FD_SET *fdw = (FD_SET*)(((char*)workmem) + size);
        FD_SET *fde = (FD_SET*)(((char*)workmem) + size * 2);
        void *dr, *dw, *de;
        int maxfd = 0;
        int j;

        fdr->fd_count = fdw->fd_count = fde->fd_count = 0;

        for (i = 0; i < count; i++) {
            int event = events[i];
            int fd = fds[i];
            if (event & ISOCK_ERECV) fdr->fd_array[(fdr->fd_count)++] = fd;
            if (event & ISOCK_ESEND) fdw->fd_array[(fdw->fd_count)++] = fd;
            if (event & ISOCK_ERROR) fde->fd_array[(fde->fd_count)++] = fd;
            if (fd > maxfd) maxfd = fd;
        }

        dr = fdr->fd_count? fdr : NULL;
        dw = fdw->fd_count? fdw : NULL;
        de = fde->fd_count? fde : NULL;

        tmx.tv_sec = millisec / 1000;
        tmx.tv_usec = (millisec % 1000) * 1000;

        select(maxfd + 1, (fd_set*)dr, (fd_set*)dw, (fd_set*)de, 
            (millisec >= 0)? &tmx : 0);

        for (i = 0; i < count; i++) {
            int event = events[i];
            int fd = fds[i];
            int revent = 0;
            if (event & ISOCK_ERECV) {
                for (j = 0; j < (int)fdr->fd_count; j++) {
                    if (fdr->fd_array[j] == (SOCKET)fd) { 
                        revent |= ISOCK_ERECV; 
                        break; 
                    }
                }
            }
            if (event & ISOCK_ESEND) {
                for (j = 0; j < (int)fdw->fd_count; j++) {
                    if (fdw->fd_array[j] == (SOCKET)fd) { 
                        revent |= ISOCK_ESEND; 
                        break; 
                    }
                }
            }
            if (event & ISOCK_ERROR) {
                for (j = 0; j < (int)fde->fd_count; j++) {
                    if (fde->fd_array[j] == (SOCKET)fd) { 
                        revent |= ISOCK_ERROR; 
                        break; 
                    }
                }
            }
            revents[i] = revent & event;
            if (revent) retval++;
        }
        #endif
    }

    return retval;
}
```

这就是我目前用的方法，刚好一百多行，这个方法我测试过，在我的台式机上同时维护一万个 socket 连接问题不大，做 echo server，每个连接每秒一条消息往返，只是 CPU 占用回到 70% 左右。

对于 Windows 下的客户端程序，维护的连接不多，这个函数足够用；而对于服务端程序，则可以做到能跑，可以让你平时跑在 Linux 下的服务端程序保证能在 Windows 下正常工作，正常开发调试，不论连接有多少。

这个方法唯一问题是 CPU 占用过高，那么 Windows 下面是否有像 kevent/epoll 一样丝滑的异步事件模型，既能轻松 hold 上万的套接字，又不费 CPU 呢？当然有，但是在说方案三之前先说两个错误的例子。

#### 错误的选择：WSAEventSelect 和 WSAAsyncSelect 

不少人提过函数 `WSAEventSelect`，它可以把套接字事件绑定到一个 `WSAEVENT` 上面：

```cpp
int WSAAPI WSAEventSelect(
  [in] SOCKET   s,
  [in] WSAEVENT hEventObject,
  [in] long     lNetworkEvents
);
```

这个 `WSAEVENT` 是一个类似 `EVENT` 的东西，看起来好像没有 `FD_SETSIZE` 的个数限制，但问题 `WSAWaitForMultipleEvents` 里你同样面临 `WSA_MAXIMUM_WAIT_EVENTS` 的限制，在 `winsock2.h` 里：

```cpp
#define WSA_MAXIMUM_WAIT_EVENTS (MAXIMUM_WAIT_OBJECTS)
```

后面这个 MAXIMUM_WAIT_OBJECTS 的数量就是 64，你还是跳不开。另外一个函数 `WSAAsyncSelect` 可以把 socket 事件关联到窗口句柄上：

```cpp
int WSAAsyncSelect(
  [in] SOCKET s,
  [in] HWND   hWnd,
  [in] u_int  wMsg,
  [in] long   lEvent
);
```

这的确没有个数限制了，问题是你需要一个窗口句柄 `HWND`，你需要创建一个虚拟窗口，那么为了模拟 posix 的 poll 行为，你打算把这个虚拟窗口放哪里呢？它的消息循环需要一个独立的线程来跑么？

Unix 的哲学是一切皆文件，Windows 的哲学是一切皆窗口，没想到有一天写网络程序也要同窗口打交道了吧？总之也是个不太干净的做法。

#### 方法3：用 iocp 实现 epoll

是的可以用 iocp 完全模拟实现 epoll，让你拥有一个高性能的 reactor 事件模型，轻松处理 10w 级别的套接字，听起来很诱惑但是很难实现，没关系，有人帮你做了：

- [https://github.com/piscisaureus/wepoll](https://github.com/piscisaureus/wepoll)

这个 wepoll 的项目意在使用 iocp 实现 Windows 下的高性能 epoll，支持 vista 以后的系统，并且只有两个文件 `wepoll.h` 和 `wepoll.c`，十分方便集成，接口也是对应 epoll 的：

```cpp
HANDLE epoll_create(int size);
HANDLE epoll_create1(int flags);

int epoll_close(HANDLE ephnd);

int epoll_ctl(HANDLE ephnd,
              int op,
              SOCKET sock,
              struct epoll_event* event);

int epoll_wait(HANDLE ephnd,
               struct epoll_event* events,
               int maxevents,
               int timeout);
```

完全跟 epoll 一样用就完事了，不过只支持 Level-triggere 不支持 Edge-triggered，不过有性能测试表明 Edge-triggered 并没有太大优势，且并不跨平台，kevent, pollset, devpoll 这些都这个模式，所以用 Level-triggered 问题不大。


#### 话题总结

那么假设你在做一个跨平台的 poll 模块，在 Windows 下上面的三套方案用哪套好呢？我的做法是内部实现的是第二套方案自定义 `fd_set`，它可以兼容到 Windows 95，算是个保底的做法，同时提供插件机制，可以由外部实现来进行增强。

然后主程序检测到系统在 vista 以后，并且包含了 wepoll 的时候，把 wepoll 的实现做一层插件封装安装进去。

