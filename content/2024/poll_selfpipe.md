---
uuid: 3163
title: 异步事件模型的 Self-pipe trick
status: publish
categories: 网络编程
tags: 网络
slug: 
date: 2024-11-04 11:41
---
异步事件模型中有一个重要问题是，当你的 select/poll 循环陷入等待时，没有办法被另外一个线程被唤醒，这导致了一系列问题：

1）在没有 pselect/ppoll 的系统上，信号无法中断 select/poll 等待，得不到即时处理；
2）另一个线程投递过来的消息，由于 select/poll 等待，无法得到即时处理；
3）调短 select/poll 的超时时间也无济于事，poll 的超时精度最低 1ms，粗糙的程序可能影响不大，但精细的程序却很难接受这个超时；
4）有的系统上即便你传了 1ms 进去，可能会等待出 15ms 也很正常。

比如主线程告诉网络线程要发送一个数据，网络线程还在 select/poll 那里空等待，根本没有机会知道自己自己的消息队列里来了新消息；或者多个 select/poll 循环放在不同线程里，当一个 accept 了一个新连接想转移给另一个时，没有办法通知另一个醒来即时处理。

解决这个问题的方法就叫做 self-pipe trick，顾名思义，就是创建一个匿名管道，或者 socketpair，把它加入 select/poll 中，然后另外一个线程想要唤醒它的话，就是往这个管道或者 socketpair 里写一个字节就行了。

类似 java 的 nio 里的 selector 里面的 `notify()` 函数，允许其他线程调用这个函数来唤醒等待中的一个 selector。

具体实现有几点要注意，首先是使用 `notify()` 唤醒，不用每次调用 `notify()` 都往管道/socketpair 里写一个字节，可以加锁检测，没写过才写，写过就不用写了：

```cpp
// notify select/poll to wake up
void poller_notify(CPoller *poller) {
    IMUTEX_LOCK(&poller->lock_pipe);
    if (poller->pipe_written == 0) {
        char dummy = 1;
        int hr = 0;
    #ifdef __unix
        hr = write(poller->pipe_writer_fd, &dummy, 1);
    #else
        hr = send(poller->pipe_writer_fd, &dummy, 1);
    #endif
        if (hr == 1) {
            poller->pipe_written = 1;
        }
    }
    IMUTEX_UNLOCK(&poller->lock_pipe);
}
```

大概类似这样，在非 Windows 下面把 `pipe()` 创建的两个管道中的其中一个放到 select/poll 中，所以用 `write()`，而 Windows 下的 select 不支持放入管道，只支持套接字，所以把两个相互连接的套接字里其中一个放入 select。

两个配对的管道命名为 reader/writer，加入 select 的是 reader，而唤醒时是向 writer 写一个字节，并且判断，如果写过就不再写了，避免不停 notify 导致管道爆掉，阻塞线程。

而作为网络线程的 select/poll 等待，每次被唤醒时，甭管有没有网络数据，都去做一次管道复位：

```cpp
static void poller_pipe_reset(CPoller *poller) {
    IMUTEX_LOCK(&poller->lock_pipe);
    if (poller->pipe_written != 0) {
        char dummy = 0;
        int hr;
    #if __unix
        hr = read(poller->pipe_reader_fd, &dummy, 1);
    #else
        hr = recv(poller->pipe_reader_fd, &dummy, 1);
    #endif
        if (hr == 1) {
            poller->pipe_written = 0
        }
    }
    IMUTEX_UNLOCK(&poller->lock_pipe);
}
```

每次 select/poll 醒来，都调用一下这个 `poller_pipe_reset()`，这样确保管道里的数据被清空后，就可以复位 `pipe_written` 标志了。

让后紧接着，处理完所有网络事件，就检查自己内部应用层的消息队列是否有其他消息投递过来，再去处理这些事件去；而其他线程想给这个线程发消息，也很简单，消息队列里塞一条，然后调用一下 `notify()`，把该线程唤醒，让他可以马上去检查自己的消息队列。

主循环大概这样：

```cpp
while (is_running) {
    // 1）调用 select/poll 等待网络事件，超时设置成 1ms-10ms；
    // 2）醒来后先处理所有网络事件；
    // 3）如果和上次等待之间超过 1毫秒，则马上处理所有时钟超时事件；
    // 4）检查自己消息队列，并处理新到来的事件。
}
```

差不多就是这样。

PS：有人说用 eventfd 也能实现类似效果，没错，但不能跨平台，只有 Linux 特有，而且还有一些坑，但 self-pipe trick 是跨平台的通用解决方案，不管你用 Windows / FreeBSD / Linux / Solaris 都可以使用这个功能。

