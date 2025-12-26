---
uuid: 3650
title: 如何清理你的系统盘（C: 盘)？
status: publish
categories: 随笔
tags: Win32
slug: 
date: 2025-12-27 00:32
---
就一年没清理 C 盘，今天清理出 140GB 的东西来，而且还没影响使用，所有程序都在往你的 C 盘拉屎。不要网友问我怎么清理下来的：

1）右键 C 盘属性，清理；
2）自己到 TEMP 目录手动清空，注意有三个 Temp：AppData 下面两个，Windows 目录下有一个；
3）SpaceSniffer 找占用大的目录，清空不合理的，这个需要一点经验，拿不准可问下 AI 某目录能不能清空；
4）清浏览器缓存；
5）最后 CCleaner 跑一遍。

![](https://skywind3000.github.io/images/blog/2025/winclean1.png)

上面一系列任务做完基本就清理出 100GB 的内容了，然后再使用 Dism++ 删除系统还原点后，又多出 40GB 来：

![](https://skywind3000.github.io/images/blog/2025/winclean2.png)

最开始剩余空间只有 130GB，现在有 272GB 剩余，可以做一次年度全盘备份了。

