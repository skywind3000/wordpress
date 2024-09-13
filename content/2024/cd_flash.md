---
uuid: 2854
title: CD3：Flash 开发宝典
status: publish
categories: 未分类
tags: 神兵利器
slug: 
date: 2024-06-25
---
前段时间碰到个经典的 Flash 游戏想玩一下，发现原网站挂了而游戏又需要验证原网站，于是想对其稍加修改，才发现原来可以下载 Flash 相关开发工具的页面已经全停了：

![](https://skywind3000.github.io/images/blog/2024/flash/flash1.jpg)

所有 Adobe 官网可以下载 flash 插件，播放器，SDK，Flash Builder 之类的地方，全被替换成了上面的页面，也就是说今天 2024 年你已经无法从官方渠道再获得一套完整的 Flash 开发环境了，而其他网站但凡提及这些资源的，都是指向了官方地址，也都会被重定向到上面的内容。

于是我想，趁着现在部分网络资源还未失效，以及我老电脑里还有一些资料，是时候对整套 Flash 开发环境进行一次整理和快照了，避免将来有一天想编译一下老项目出现尴尬。

本光碟包含 Flash 全胜时期的完整开发环境，包含 Flex 各版本 SDK，AIR 运行时和 SDK，各版本播放器，相关工具，以及经典轻量级 IDE - FlashDevelop：

![](https://skywind3000.github.io/images/blog/2024/flash/flash2.png)

虽然 Flash 官配 IDE 是 Flash Builder，但懂行的都知道，那玩意儿臃肿庞大不说，项目稍微一大点，就会卡到没法用，所以真的动手，大都会使用更加小巧流畅的 FlashDevelop。

（点击 more/continue 继续）

<!--more-->

#### 光盘目录

内容表格：

![](https://skywind3000.github.io/images/blog/2024/flash/table1.png)

还有其它一些实用工具隐藏于各个目录之间，表格里写不下了，可以自行探索。

#### IDE

开源免费的 FlashDevelop 不仅启动快速、运行流畅，还有丰富的插件扩展：

![](https://skywind3000.github.io/images/blog/2024/flash/flash3.png)

整个安装包也只有 26MB，使用的话请参考光盘根目录下面的《环境搭建说明》文档即可。

#### SDK

光盘内包含了两套整合了 FlexSDK 和 AIR SDK 的工具链：

![](https://skywind3000.github.io/images/blog/2024/flash/table2.png)

每套工具都可以输出最高版本以下的 .swf 文件，比如用 FlexSDK27 也可以输出支持 Flash Player 14.0 的 .swf 文件，之所以包含两套是因为国内不少游戏是 16 写的，16 版本的 SDK 基本算是千锤百炼了，如果你用了很多年 16 的，那用它不会有任何意外。

如果没历史负担，直接用 27 版本的即可。

#### Flash Player

本光盘包含下面几个版本的独立播放器，搭配 FlashDevelop 开发调试使用：

![](https://skywind3000.github.io/images/blog/2024/flash/flash4.png)

推荐的话，就用 29 版本的就行，29 是官方最后一个没广告不会强制你更新的播放器了，后面 30-32 都在搞广告和重定向到中国版 Flash 那一套。

比如 Adobe 官方最后的播放器是版本 32 的，如果国内使用不进行一些网络屏蔽的话，稍微跑两秒钟就告诉你不能用了，要更新：

![](https://skywind3000.github.io/images/blog/2024/flash/flash5.png)

诱导你去下载国内特供版，而 29 的话，功能上基本上是最新的，也是最后一个没有强制更新和弹广告的官方播放器了。其中 34 版本，是国内特供版的去广告绿化版本，我用着没啥问题，大家也可以一试。这些播放器非常难找，Adobe 官网停掉了，网上还能找得到的只有 32/34 了，我找到这些独立播放器版本非常不容易。

我碰到过个别老游戏，最新版播放器反而有问题，这时 14 版本的播放器反而是对老游戏兼容性最好的一款了。

#### 增强插件

光盘内包含了几款 FlashDevelop 的经典插件，比如 NavigationBar：

![](https://skywind3000.github.io/images/blog/2024/flash/flash6.png)

它会在源码窗口上方增加两个下拉框，可显示当前类和方法，也可按类和方法快速跳转；另一个叫做 QuickNavigate 的插件，可以允许使用 CTRL+鼠标左键点击符号进行跳转。

还有一个叫做 swcbuild 的插件，可以在新建项目时提供一种新的构建 .swc 的项目类型，避免使用 ant，因为 FlashDevelop 里默认新建 .swc 时是需要使用 ant 来构建的。

上面三个插件都比较趁手，推荐安装，另外还有一些选择性安装的插件可以自己探索。

#### Java Runtime

因为 Flex SDK 需要 JRE，而且是 32 位的 JRE，但大部分人机器上安装的可能是 64 位的 JRE，因此光盘里配套了一份 32 位的 JRE，保证你在断网的情况下也能使用本光碟将环境搭建起来，当然你有网络的话，也可以下载安装最新的 32 位 JRE：

https://www.java.com/download/manual.jsp

到上面地址，注意选择 32 位的 Windows Offline 安装包。

#### 电子书

本光碟的制作原则是 “断网可用”，那么断网的情况下进行 Flash 开发的话，没法查询在线帮助，当然需要一本离线的类库参考手册：

![](https://skywind3000.github.io/images/blog/2024/flash/flash7.png)

Flash 的参考手册有很多，这是我找的最好的一个版本，基本把 Adobe 官网的帮助给帮运下来了，坐上方是选择包名，左下方是选择类，正上方是导航，选择导航栏的 “索引” 可以在左下角搜索框里按照关键字搜索内容：

![](https://skywind3000.github.io/images/blog/2024/flash/flash8.jpg)

另，目前这份参考手册的官方网站还没有失效，有需要还可以查看最新的内容：

- [ActionScript Reference - EN](https://help.adobe.com/en_US/FlashPlatform/reference/actionscript/3/index.html)
- [ActionScript Reference - CN](https://help.adobe.com/zh_CN/FlashPlatform/reference/actionscript/3/index.html)

上面两个地址一个英文，一个中文，希望能多存活一段时间，除此之外还有一份简要的 ActionScript3 语法手册和 Adobe 出版的一本 AS3编程电子书，即便将来有一天网上的资料全部失效了，这三分文档也能帮你迅速开始开发。

#### 常用工具

光盘内包含很多常用工具，比如反编译器：jpexs-decompiler

![](https://skywind3000.github.io/images/blog/2024/flash/flash9.jpg)

将 .swf 转换成可执行程序的：Projector Tools

![](https://skywind3000.github.io/images/blog/2024/flash/flash10.jpg)

原理就是 Flash 独立播放器运行时，其实会检查当前可执行文件末尾是否包一块固定大小和标志的表格，如果包含的话，进一步检查时候代表有追加 .swf 有的话就会自动加载。

也就是说将 .swf 转换成 .exe 时只需要将 .swf 的内容附着在播放器可执行文件末尾，然后再附加一个表格说明 .swf 文件长度等信息即可，而这个 Projector Tools 就是做这个的。

而另外一个 EXE2SWF 可以用来将 EXE 内包含的 .swf 反解出来，而 SolEditor 用于编辑 Flash 游戏的存档文件，这些只是一部分，更多工具欢迎自己探索。

#### 后记

Flash 技术影响深远，今天 H5 多少功能都是抄袭当年的 Flash，包括现在火热的WASM，对标的也是 Flash 早在 2012 年就搞出来的允许 C 代码编译成 AVM2 虚拟机字节码的 CrossBridge 技术，今天各大直播网站，接口的也还是 Flash 发明的 RTMP 视频流传输协议。

当年乔布斯攻击 Flash 说什么在 Safari 下用 Flash 看视频发热量很大，事后查证，因为 Flash 团队多次要求苹果 Safari 给他们开放硬件加速接口而遭到拒绝导致，只能说商战有时候也很恶心，而 Adobe 自己也不争气，为了点蝇头小利而固步自封，假设 2010 年时能把 Flash 做成开放标准，也许也不没今天 H5 什么事情。

不过也不妨碍今天抱着欣赏和怀旧的心情来制作这张光碟。

#### 下载地址：

- 度盘：地址 `s/1WeD1T8s3iWIRVEW3pAiGfw`，口令 `4waf`
- 115：地址 `s/swzra4b3ze9` ，口令 `8866`
- 谷歌：[FlashDevelop.iso](https://drive.google.com/drive/folders/16LtsaqRWMDJ3VKaDFaIWidKLZ2Z7cI5s?usp=sharing)

防止机器人扫描，度盘自行添加 https://pan.baidu.com/ ，115 自行添加 https://115.com/ 即可。


永久地址（防止上面失效），欢迎关注绝版软件保护工程：

https://github.com/skywind3000/preserve-iso


往期回顾：

- [CD1：Borland 宝典](/blog/archives/2607)
- [CD2：SharpDevelop](/blog/archives/2852)
- [CD3：Flash 开发宝典](/blog/archives/2854)
- [CD4：WinXP 开发宝典](/blog/archives/2808)



