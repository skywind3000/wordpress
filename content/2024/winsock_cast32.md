---
uuid: 3132
title: WinSock 可以把 SOCKET 类型转换成 int 保存么？
status: publish
categories: 网络编程
tags: 网络,Win32
slug: 
---
在 Linux/Unix 等 posix 环境中，每个套接字都是一个文件描述符 `fd`，类型是 `int`，使用起来非常方便；但在 Win32 环境中是 `SOCKET` 类型被定义成  `UINT_PTR` ，是一个指针，在 x64 环境中一个 `SOCKET` 占用 8 个字节。

那么是否能将 `SOCKET` 类型强制转换成 `int` 类型保存没？这样就能统一用 `int` 在所有平台下表示套接字了，同时在 x64 环境下这样将 64 位的指针转换为 32 位的整数是否安全？

答案是可以的，下面将从三个方面说明一下。

#### Kernel Object

每个 SOCKET 背后其实都是一个指向 Kernel Object 的 Handle，而每个进程的 Handle 的数量是有限的，见 MSDN 的 [Kernel Objects](https://learn.microsoft.com/en-us/windows/win32/sysinfo/kernel-objects)：

> Kernel object handles are process specific. That is, a process must either create the object or open an existing object to obtain a kernel object handle. The per-process limit on kernel handles is 2^24. However, handles are stored in the paged pool, so the actual number of handles you can create is based on available memory. 

单进程不会超过 2^24 个，每个 Kernel Object 需要通过一个 Handle 来访问：

![](https://skywind3000.github.io/images/blog/2024/win32/cshob-04.png)

这些 Handle 保存于每个进程内位于低端地址空间的 Handle Table 表格，而这个 Handle Table 是连续的，见 MSDN 中的 [Handles and objects](https://learn.microsoft.com/en-us/windows/win32/sysinfo/handles-and-objects)：

> Each handle has an entry in an internally maintained table. Those entries contain the addresses of the resources, and the means to identify the resource type.

这个 Handle Table 表格对用户进程只读，对内核是可读写，在进程结束时，操作系统会扫描整个表格，给每个有效 Handle 背后指向的 Kernel Object 解引用，来做资源回收。

所以看似是 `UINT_PTR` 指针的 `SOCKET` 类型，其实也只是一个表格索引而已，这个 Handle Table 表格的项目有数量限的（最多 2^24 个元素），内容又是连续的，那当然可以用 `int` 来保存。


#### 开源案例

故此不少开源项目也会选择在 Windows 环境下将 `SOCKET` 类型直接用 `int` 来存储，比如著名的 openssl 在 [include/internal/sockets.h](https://github.com/openssl/openssl/blob/59f5f6c73cd2e1e2bd8ef405fdb6fadf0711f639/include/internal/sockets.h#L53-L62) 里有解释：

```cpp
/*
 * Even though sizeof(SOCKET) is 8, it's safe to cast it to int, because
 * the value constitutes an index in per-process table of limited size
 * and not a real pointer. And we also depend on fact that all processors
 * Windows run on happen to be two's-complement, which allows to
 * interchange INVALID_SOCKET and -1.
 */
#   define socket(d,t,p)   ((int)socket(d,t,p))
#   define accept(s,f,l)   ((int)accept(s,f,l))
```

所以 openssl 不论什么平台，都将套接字看作 `int` 来使用：

```cpp
int SSL_set_fd(SSL *ssl, int fd);
int SSL_set_rfd(SSL *ssl, int fd);
int SSL_set_wfd(SSL *ssl, int fd);
```

所以它的这些 API 设计，清一色的 `int` 类型。


#### 程序验证

道理前面都讲完了，下面写个程序验证一下：

<!--more-->

```cpp
void create(int n) {
    std::vector<SOCKET> sockets;
    for (int i = 0; i < n; i++) {
        SOCKET s = socket(AF_INET, SOCK_STREAM, 0);
        if (s == INVALID_SOCKET) {
            printf("socket failed with error %d\n", WSAGetLastError());
            break;
        }
        sockets.push_back(s);
        printf("index=%d socket=%llu\n", i, (uint64_t)s);
    }
    for (int i = 0; i < n; i++) 
        closesocket(sockets[i]);
    printf("\n");
}

int main(void) {
    WSADATA WSAData;
    WSAStartup(0x202, &WSAData);

    printf("Round 1:\n");
    create(10);

    printf("Round 2:\n");
    create(10);
    return 0;
}
```

在 64 位环境下，创建 10 个套接字，然后释放，再创建 10 个：

```
Round 1:
index=0 socket=352
index=1 socket=324
index=2 socket=340
index=3 socket=332
index=4 socket=336
index=5 socket=356
index=6 socket=360
index=7 socket=364
index=8 socket=368
index=9 socket=372

Round 2:
index=0 socket=372
index=1 socket=368
index=2 socket=364
index=3 socket=360
index=4 socket=376
index=5 socket=356
index=6 socket=336
index=7 socket=332
index=8 socket=340
index=9 socket=324
```

可以看出，即便在 64 位下面：1）`SOCKET` 指向的表格项目是连续的；2）前面释放掉的表格项目，是会被后面复用的；3）他们都在表格范围内，不会由于不停创建/销毁导致 `SOCKET` 的数值持续增长。

成功的印证了前面关于 Kernel Object 和 Handle Table 的解释。


