---
uuid: 3035
title: 库代码中是否应该检查 malloc 的返回值？
status: publish
categories: 编程技术
tags: 系统开发
slug: 
date: 2023-09-03 21:56
---
现在网上有很多似是而非的观点，比如 malloc 失败不用处理，直接退出，这样的经验看似很聪明，实际却很局限，比如：

1）嵌入式设备：不是所有设备都能有一个强大的全功能的操作系统，也不是所有设备都能有虚拟内存功能。

2）长时间运行的程序，内存虽然够，但由于碎片，会导致没有连续足够大的线性地址进而分配失败，32 位程序特别明显。

3）管理员对某类进程设置过内存限制，比如某类要起很多个的进程，那么设置一下内存限制是一个很正常的操作。

4）程序通过容器运行，事先给定了最大内存用量。

5）操作系统 overcommit 选项被管理员关闭。

所以说 malloc 失败不用检测，大多数是明确知道自己运行环境的某一类程序，比如上层业务，比如 CRUD，比如你就是做个增删改查，知道自己运行于一台标准的 linux 服务器，那么确实无需多处理，崩了也就崩了；或者你的程序严重依赖 malloc 三行代码一次分配，那么即使恢复出来估计你也很难往下走，不如乘早崩溃，免得祸害他人。

上面这些情况确实可以简单粗暴处理，但如果你开发一些基础库，你没办法决定自己是会运行在一台标准服务器上还是某个小设备里，那么上面的经验就完全失效了。

比如你开发一个类似 libjpeg 的图象编解码库，你没法假定运行环境，那么 malloc 失败时，你是该自作主张直接 assert 强退掉呢？还是该先把分配了一半的各种资源释放干净，然后向上层返回错误码，由上层决定怎么处理比较好呢？比如上层可选择：1）报错退出；2）释放部分缓存后再运行；3）降级运行，比如图象编码使用 low profile 再运行一遍。

你作为图象编码库需要经常分配一些比较大块的内存，你这里失败了，不代表上层无法继续分配内存处理后续任务对不对？上层内存里有很多图片 cache 用于加速图片显示，你这里失败了，上层感知到，直接从 cache 里回收一波，内存就又有了，对不对？图象视频编码根据资源消耗高低都有 high profile, low profile 的运行模式，你 high profile 内存不够了报告上层，上层视情况还可以选择再用 low profile 跑一遍对不对？

就是上层什么都不做，只在检测到你的返回值时在日志里记录一行内存不够再退出，你也得给上层一个选择的权利，而不是不管不顾，直接退掉；所以，你一个库碰到这类问题还是要自己处理干净把错误返回给上层，让上层来判断该如何处理更恰当一些。

再一种是需要精细控制内存的应用层业务，比如自己主动管理多个内存池，栈上的池不够了就应该到堆上的堆上池分配，堆上池分配不了就应该回收，回收不了就向操作系统要新的，这种情况也不能一概而论。

那么是不是说所有的 malloc 都要去处理 NULL 返回？当然不是，这里强调的是你既然选择用 C 语言了，脑袋里要有根弦，知道这个问题需要分情况处理，区分得了哪些代码重要，哪些代码不重要；哪些代码要什么力道去写，写到多深，这样即使某些业务模块懒得处理了，不处理 NULL 或者写个 assert 也没问题，但如果头脑里没这跟弦，不知道不同层次的代码需要不同的力道去写，一概无脑的不处理或者 assert，那么这样的代码写多了，只会越写越笨。


