---
uuid: 3683
title: 要从vim切换到neovim吗？
status: publish
categories: 随笔
tags: Vim
date: 2025-01-25 23:48
---
很多人问我为啥我用 vim 而不用 neovim，这里统一回答下吧我用 vim 就是图 “稳定” 两个字：vim 每个新功能都要加一堆测试，测试覆盖率在 vim9 之前达到 93%，后面开发了 vim9script 以后，覆盖率一度掉到 79%，但现在又在慢慢回升到 82%；而 neovim 天天忙着开发新功能，对老功能的维护很不上心，比如下面这个 bug：

![](https://skywind3000.github.io/images/blog/2025/neovim1.png)

如图：Neovim 在 Windows 下面根本无法区分正斜杠反斜杠，以及不同大小写，同样的文件被当成多份不同的内容，导致历史搜索全废，比如你想查看下 `v:oldfiles` 结果：

![](https://skywind3000.github.io/images/blog/2025/neovim2.png)

Neovim 再 Windows 下文件路径分隔符不同，会被当成不同的文件，搞笑吧？已经影响正常使用了，每次打开 telescope 的查找旧文件，经常一堆重复命名，原来是 nvim 里的 v:oldfiles 机制就出问题了，没法区别，我提了两年没人修。

有人说 vim 开发新功能慢，这恰恰是 vim 更重视稳定性的表现，很多人可能不知道 neovim 天天都在从上游 vim 导入质量修正的 patch，比如下面这些：

![](https://skywind3000.github.io/images/blog/2025/neovim3.jpg)

你们可以去读读 neovim 的更新日志，动不动就是这种 "vim-patch:9.1.1033" ，代表 neovim 又从 vim 那里 import 了一个质量 patch，而总共导入了 13031 条，以 neovim 这种天天飙新功能不顾老功能的尿性，要是 vim 不在前面不停的完善稳定性，neovim 质量早蹦了，而 neovim 自己专有代码由于没法导入上游的 patch 了，质量常常难以言说，上面的 bug 就是个例子。

PS：neovim 的有几个开发，天天一边骂 vim 一边天天从 vim 导入 patch，玩的真溜，其中几个我是感觉人品有点问题的。

其次，不重维护，比如 nvim 的文档编写简直是惜字如金，光内置终端的使用和相关 API 说明，这么重要的功能但 nvim 的文档只有区区不到 200 行，作为插件作者，给 nvim 写插件碰到问题查文档是不行的，经常要去 issue 里搜索才知道，对比下来 vim 里内置终端的文档有整整 2000 行，看完再也不用去网上搜索半天。

比如当年一个例子，在 0.8.0 以前 nvim 要判断是否运行于 gui 有多麻烦？文档里不会告诉你，我在论坛上搜半天搜到了 justinmk 给的方案：

<!--more-->

![](https://skywind3000.github.io/images/blog/2025/neovim4.jpg)

这么恶心，被一堆人骂了几年以后它们终于同 gvim 一样支持了 has('gui_running') 检测了，这样的例子数不胜数，还有好多没改的。

再者，nvim 经常 break 东西，从 nvim 自己的 api 开始，内置 cscope 这么重要的一个功能，说砍就砍，连个投票调查都没有，就 issue 里两个人聊了两句就 tm 砍掉了，他们不知道目前 LSP 在阅读大型复杂代码库时力所不及么？他们觉得自己没需求所有人都没需求了？问都不问一句。

最后，nvim 的整个插件体系也经常 break 东西，我经常一两个月用下 nvim 体验下最新功能，update 一下插件，结果往往隔月 update，就会碰到插件的 breaking changes，导致我的配置完全无法使用了，又要折腾半天，我工作忙着可没这个时间和精力，但 vim 的接口稳定到你 8.0 时代的配置现在 9.1 都能用。

总结下：除了一些表现型的界面上的东西，vim 里从内在 api 和机制上来讲，并没有什么事情只有 neovim 能做而 vim 不能做，而我又更看重稳定性，所以我把 neovim 看成是一个 alpha 版的 vim，喜欢尝鲜，不注意质量，天天有时间折腾的人适合使用。



--

出门右转：今天数了一下，我给 vim/neovim 开发的插件，居然超过 20 个了：

- https://skywind.me/wiki/vim_plugins



