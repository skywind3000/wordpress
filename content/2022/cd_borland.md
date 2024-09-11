---
uuid: 2607
title: CD1：BORLAND 宝典
status: publish
categories: 未分类
tags: 神兵利器,GUI
slug: 
date: 2022-04-06 17:45
---
图形界大佬 John Carmack 在推特上呼吁大家，现在应该有意识的保存你的开发环境，这样多年以后你想重新构建你的软件时才不会慌脚乱手，因为通常每过几年你常常会发现，自己之前的老代码已经没有合适的环境编译了：

![](https://skywind3000.github.io/images/blog/2022/borland_1.jpg)

今天互联网上的内容，由于各种原因，正在以越来越快的速度消失，而习惯什么都从网上找的新一代网民们，却并没有备份和记录的习惯及意识。不远的将来，会有一天，当你特别想找某个工具却搜尽互联网你都找不到时，就麻烦了。

这是一张兼具收藏价值和实用价值的光碟，收录了 Borland 公司全胜时期的著名桌面开发工具：C++ Builder 6 和 Delphi 7，以及各种配套书籍和资源，都是全网最好的版本（原版 CD 安装文件加最新补丁）。别看这两款软件老，因为生成可执行独立小巧，至今依然可以用他们做出交互尚可的桌面应用。

他们最大的特点，是可以让你轻松开发出 1MB 以内的无依赖的桌面软件：（点击 Read more 展开）

<!--more-->

![](https://skywind3000.github.io/images/blog/2022/borland_2.png)

今天你用 VS2022 的 MFC 开发个程序，静态链接都要 2MB，关键是开发效率 BCB6 / DELPHI7 比 MFC 快多了，随便拖拖控件 200KB 的独立可执行，可以在 Windows XP 这样的老电脑上完美运行：

![](https://skywind3000.github.io/images/blog/2022/borland_3.jpg)

觉得经典风格控件不好看？没关系，可以使用 Windows 系统自带的 Visual Style 风格化控件。

#### 可视化风格

Windows XP 以后有一套叫做 [Visual Style](https://learn.microsoft.com/en-us/windows/win32/controls/visual-styles-overview) 的机制，只需要在可执行的 `manifest` 配置里打开即可：

![](https://skywind3000.github.io/images/blog/2022/borland_4.jpg)

这样在 XP/Vista/Win10 下就会显示对应风格的控件，使用很简单，编辑一个 manifest 文件（具体见光盘内文档），当作资源添加到项目里即可，然后上面的窗口立马变身：

![](https://skywind3000.github.io/images/blog/2022/borland_5.jpg)

在 Windows 7 下面，效果对比，看起来还行：

![](https://skywind3000.github.io/images/blog/2022/borland_6.jpg)

Windows 10 下效果对比，看起来不错：

![](https://skywind3000.github.io/images/blog/2022/borland_7.jpg)

用几百 KB 的可执行，做现代风格的桌面程序，效果还行吧？

#### 皮肤引擎

还不满足的话，光盘里还带着著名皮肤库：VCLSkin 5.60

![](https://skywind3000.github.io/images/blog/2022/borland_8.jpg)

可以安装到 BCB6 / D7 的控件面板里，使用时从面板里将 VCLSkin 的控件拖到窗口上，属性那里设置下皮肤文件就行，F9 编译，一键换肤，同时自带 200+ 套皮肤文件和皮肤编辑器 Skin Builder，满足你的定制需求。

皮肤引擎有很多，VCLSkin 是最有名的实现，而网上有很多版本，这是最新最完整的 5.60 ，包含皮肤制作工具，代码，文档和 Demo。

#### 版本选择

基本都是选择的最纯净的光盘安装文件提取，没有任何病毒，同时还附带了升级补丁，比如 BCB6 的 Update Pack4，是最后的 BCB6 补丁了，它包含了 26 项更新（光盘版是 Build 10.157 升级 UP4 以后是 10.166）。基本上 Borland 或者 Embarcadero 的官网都下载不到，费了非常大的力气才找到的更新补丁。网上很多 BCB6 基本都是一个安装包就没了（10.157），根本没有这个 Update Pack 4 不说，有些还有病毒。

同时 Delphi 除了光盘安装版外，还附带了一个绿色版 Delph7-Lite，集成了众多补丁和专家工具，还移植了 Delphi 2007 的 RTL/VCL/zlib 等众多库（D7 支持的）。这个 Delphi7-Lite 非常有名，网上一搜便知，但是网上流传的较多的是比较老的 2008 或者 2010 年的版本，作者一直在更新的，光碟内的是 2011 年最终版本。

Delphi7-Lite 还有一个问题是能在 Win7 下安装，在 Win10 下面安装会报错，顺手帮他解决了。敢叫 “Borland 宝典”，必然是下了功夫的。

#### 文档资源

有人说，忘记了怎么写 BCB6/D7 怎么办？没问题，光盘内自带若干学习资料：

![](https://skywind3000.github.io/images/blog/2022/borland_9.jpg)

还有 Delphi 7 的，更丰富，比如水木清华 BBS Delph 面板的所有精华帖：

![](https://skywind3000.github.io/images/blog/2022/borland_10.jpg)

从 Object Pascal 到 VCL 控件使用，还有各种使用技巧，应有尽有，根本不用到网上查。

#### 图标资源

那么有了皮肤库，有了学习资料，要真的上手开发桌面应用还需要什么呢？没错，图标库：

![](https://skywind3000.github.io/images/blog/2022/borland_11.jpg)

包含各种常用风格的图标，一样不用到网上找来找去，还不满足的话可以下载 10 万图标合集 Pichon。

#### 绝版资源

作为一张兼具收藏价值和实用价值的光碟，包含了 Borland 曾经免费发布过如今很难找到的 Borland C++ Compiler 5.5 命令行编译器，还有后面 Embarcadero 发布的 Embarcadero C++ 10.2 Command-line Compiler，这两个都是 C++ Builder 对应版本的独立编译器，非常小巧，前者 5MB，后者 18MB。

如今有点什么小需求，不喜欢安装 20GB 的 Visual Studio 或者 1-2GB 的 MINGW 的话，可以用他们开发标准的 Windows 程序，无需安装，解压就用。

#### 珍藏资料

怀旧就要彻底，本光碟包含一份 DOSBOX 环境，可以让你方便的体验到 BORLAND 早年一系列开发工具：

![](https://skywind3000.github.io/images/blog/2022/borland_12.jpg)

> Turbo Pascal 7：编译快占用少，很多 NOI 选手当年就在软盘上跑 TP7，编译很少读盘

很多人都用过 DOS 下的 Turbo C 2.0，但是 DOS 下最好用的 C++ IDE 是 Borland C++ 3.1，估计用过的人就不多了：

![](https://skywind3000.github.io/images/blog/2022/borland_13.jpg)

同时打开多个文件，多文档窗口（MDI），支持窗口扩大缩小，移动，互相覆盖，支持鼠标，源代码有语法高亮，比 Turbo C 2.0 强大太多了。

DOS 环境还除了 Borland 的软件外，还包含同期一些很珍贵的软件，完整清单：

![](https://skywind3000.github.io/images/blog/2022/borland_14.jpg)

这些软件都不大，所以顺便收录了以下，加起来基本上是一个完整开发环境了，整个打包下来 28MB，十分小巧。所用的模拟环境不是常年不更新的老旧的 DOSBox 而是最新的继承者 DOSBox-X，窗口可以随意缩放。

#### Lazarus IDE

附带 Delphi 的开源继承者 Lazarus 2.2，使用 free pascal + free vcl 的跨平台 Rad 开发工具：

![](https://skywind3000.github.io/images/blog/2022/borland_15.jpg)

对于喜欢 BCB6 / D7 的朋友们值得尝试一下，可以开发：Windows / Linux / MacOS 的跨平台桌面应用程序，.NET 吹了二十年的牛逼至今都没做到。

详细见介绍：[用 Lazarus 做 GUI 程序合适吗 ？](https://www.zhihu.com/question/54905309/answer/2355684869)

#### 其他资源

怀旧就要讲究个气氛，为了增加气氛，怎么能少了李维的《Borland 传奇》？

![](https://skywind3000.github.io/images/blog/2022/borland_16.jpg)

让本光碟多一点文化属性，还有其他更多内容，欢迎自行探索。

#### 光盘大小

这么一张功能齐全的怀旧开发工具大全 CD，该有多大呢？仅仅 642MB 而已：

![](https://skywind3000.github.io/images/blog/2022/borland_17.jpg)

使用标准 CD 的尺寸（<=650 MB）有几个好处，第一个是大小可控，便于存储和传输；第二是给自己设置一个限制，原本准备放的东西是 1-2GB 的，但是加上这个限制后就不得不更好的组织空间和精简内容，最终留下来的都是确实有价值，没有冗余，没法再删除一个文件的精品内容。

#### 下载地址

避免机器人扫描，读盘地址前请自己拼接 `https://pan.baidu.com/` ，115 自行添加 `https://115.com/` 即可：

- 谷歌：[BORLAND.iso](https://drive.google.com/file/d/1B60qf28kRGzXh5Ad1jYIL1j8Pyb6Mwmg/view?usp=sharing)
- 度盘：地址 `s/159NZDyQTxKln5LRYYZQMQQ`，口令 `xg5z`
- 115：地址 `s/swn1qwp3ze9`，口令 `8866`


永久地址：https://github.com/skywind3000/preserve-iso


--

有网友推荐了一个盒子论坛：[盒子论坛 v2.1](https://bbs.2ccc.com/)

是目前比较活跃的 Delphi / C++ Builder 的国内论坛，有不少精华文章和资源下载。

再推荐一个怀旧开发工具下载网站：[WinWorld](https://winworldpc.com/product/delphi/70) 。

往期回顾：

- [CD1：Borland 宝典](/blog/archives/2607)
- [CD2：SharpDevelop](/blog/archives/2852)
- [CD3：Flash 开发宝典](/blog/archives/2854)
- [CD4：WinXP 开发宝典](/blog/archives/2808)

