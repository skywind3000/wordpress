---
uuid: 2500
title: 如何实现一个真正高性能的spin_lock？
status: publish
categories: 编程技术
tags: C++,系统开发
date: 2017-02-21 00:05
slug: 
---
应用层用spinlock的最大问题是不能跟kernel一样的关中断（cli/sti），假设并发稍微多点，线程1在lock之后unlock之前发生了时钟中断，一段时间后才会被切回来调用unlock，那么这段时间中另一个调用lock的线程不就得空跑while了？这才是最浪费cpu时间的地方。所以不能关中断就只能sleep了，怎么着都存在巨大的冲突代价。

尤其是多核的时候，假设 Kernel 中任务1跑在 cpu1上，任务 2跑在 cpu2上，任务1进入lock之前就把中断关闭了，不会被切走，调用unlock的时候，不会花费多少时间，cpu2上的任务2在那循环也只会空跑几个指令周期。

看看 Kernel 的 spinlock:

```cpp
#define _spin_lock_irq(lock) \
do { \
	local_irq_disable(); \
	preempt_disable(); \
	_raw_spin_lock(lock); \
	__acquire(lock); \
} while (0)
```

看到里面的 local_irq_disable() 了么？实现如下：

```cpp
#define local_irq_disable() \
    __asm__ __volatile__("cli": : :"memory") 
```

倘若不关闭中断，任务1在进入临界区的时候被切换走了，50ms以后才能被切换回来，即使原来临界区的代码只需要0.001ms就跑完了，可cpu2上的任务2还会在while那里干耗50ms，所以不能禁止中断的话只能用 sleep来避免空跑while浪费性能。

所以不能关闭中断的应用层 spinlock 是残废的，nop都没大用。

不要觉得mutex有多慢，现在的 mutex实现，都带 CAS，首先会在应用层检测冲突，没冲突的话根本不会不会切换到内核态，直接用户态就搞定了，即时有冲突也会先尝试spinlock一样的 try 几次（有限次数），不行再进入休眠队列。比傻傻 while 下去强多了。
