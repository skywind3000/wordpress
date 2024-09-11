---
uuid: 2869
title: CD：绝版游戏保护工程
status: publish
categories: 未分类
tags: 经典游戏
slug: 
date: 2020-10-15
---
本光碟收录了 64 款几近绝版的精品 DOS 游戏，大部分游戏现在网上都很难找到。虽然 DOSBOX 可以模拟 DOS 游戏，但是不同的游戏设置不同，有的需要加载光碟，有的需要配置好声卡参数，有的游戏还需要特定的 DOSBOX 版本才能运行。

#### 光碟特点

所以整理了这份 DOS 游戏的 “64合1”，让你以最简单的方式，重温这些老游戏。同时想玩这些游戏时，再也不用到网上东找西找，找到一些捆绑流氓软件和病毒的东西。

#### 运行方式

把 GAME 目录下面的 `DOS.rar` 文件解压到任意目录：

![](https://skywind3000.github.io/images/blog/2020/cd1/cda1.png)

解压出来总共 1.3GB 的内容，进入解压后的 DOS 目录，点击 “DFend.exe” 即可运行。

#### 操作方式

DFend.exe 是一个 DOSBOX 的 GUI 前端程序，帮你方便的组织管理 DOS 游戏：

![](https://skywind3000.github.io/images/blog/2020/cd1/cda2.jpg)

直接双击运行游戏就行了，运行过程中，有一些常用的快捷键：

- ALT+ENTER：切换全屏模式和窗口模式。
- CTRL+F9：结束 DOSBOX
- CTRL+F10：释放鼠标
- CTRL+F11：降低 CPU 速度
- CTRL+F12：增加 CPU 速度

如果在游戏中觉得速度过快或者过慢，可以用 CTRL+F11/F12 进行调节，注意 DOSBOX 窗口标题栏会写着当前 CPU 的速度。

（点击 more/continue 继续）

<!--more-->

#### 游戏信息

花了不少时间给每个游戏添加上了相关信息，包括：截图、文字介绍、开发商、发行商、发布时间以及游戏类型：

![](https://skywind3000.github.io/images/blog/2020/cd1/cda3.jpg)

点击 “附注” 标签，还能看到游戏的介绍：

![](https://skywind3000.github.io/images/blog/2020/cd1/cda4.png)

#### 调整设置

选中一个游戏，右键选择 “编辑”：

![](https://skywind3000.github.io/images/blog/2020/cd1/cda5.jpg)

就会出现属性窗口：

![](https://skywind3000.github.io/images/blog/2020/cd1/cda6.jpg)

然后选择左边的 “显卡” 项目，就可以设置分辨率：

![](https://skywind3000.github.io/images/blog/2020/cd1/cda7.jpg)

因为以前的游戏分辨率太低，我默认都设置了 1366x768 的窗口，你可以按需更改。

#### DOS 环境

选择第一项 “DOSBox DOS” 按回车：

![](https://skywind3000.github.io/images/blog/2020/cd1/cda8.jpg)

就能进入 DOS 命令行环境了：

![](https://skywind3000.github.io/images/blog/2020/cd1/cda9.png)

DOS 环境下，有一些预装内容：

C: 系统工具：FREEDOS 常用工具，以及 tools 目录下面的 QBASIC, GWBASIC
D: 编程工具：Turbo C 2.0, Turbo C++ 3.0, Borland C++ 3.1, Turbo Pascal 7.0 以及打字游戏 

其中 C 盘对应 VirtualHD 目录，D 盘对应 VirtualDD 目录，你可以按需添加需要的工具进去。同时 E 盘被映射到了 Games 目录，可以直接访问本光碟中的所有游戏。

比如你想启动 Turbo Pascal 的话，输入：

```text
D:
cd \tp7\bin
turbo
```

三条命令，就能进入 turbo pascal 环境了：

![](https://skywind3000.github.io/images/blog/2020/cd1/cda10.png)

然后按 F9 编译，CTRL+F9 执行，执行太快看不到结果的话，用 ALT+F5 查看程序输出。

到 D:\TT 目录下运行 tt ，就能玩经典的打字练习了：

![](https://skywind3000.github.io/images/blog/2020/cd1/cda11.png)

除了 64 个游戏外，DOS 命令行中，C 盘和 D 盘下面还收录了不少有趣的东西。

#### 辅助工具

在 “工具” 目录中，包含了 DOSBOX 的原始工具，包括最新版的 DOSBOX 以及前端 DFend，同时 DOSSeed可以用来为单个游戏制作一个集成包，一键运行。

#### 运行环境

默认运行环境为 DOSBox，但是 2021年1月1日的版本中，引入了 DOSBox-X，这是一个 DOSBox 的一个活跃更新维护的分支，使用起来可以非常自由的在主菜单上进行配置：

![](https://skywind3000.github.io/images/blog/2020/cd1/cda12.png)

DOSBox-X 搭配一个主菜单，可以很方便的设置微调，比如目录 Video->Fit to aspect ration 就可以设置缩放时保持画面宽高比例），比如 CPU->Emulate CPU Speed 下面可以按机器型号（486 DX2 100MHz 等）设置 CPU 频率。

更方便的是 DOSBox-X 可以自由的缩放窗口大小，鼠标直接拖窗口右下角，或者点最大化按钮即可。故此在 DOS\Runtime 下面增加了 DOSBox-X 的可执行文件，同时在 DOS\Script 下面增加了各个游戏用 DOSBox-X 启动的启动脚本，方便运行。

DOSBox-X 的主要快捷键是：

- F11+F：切换全屏
- F11+ESC：显示/隐藏主菜单
- CTRL+F9：强制结束
- CTRL+F10：捕获或者释放鼠标

#### 下载地址

避免机器人扫描，读盘地址前请自己拼接 `https://pan.baidu.com/` ，115 自行添加 `https://115.com/` 即可：

- 谷歌：[绝版游戏保护工程1](https://drive.google.com/drive/folders/1FA5Md3wEz9ha4ThEfCcd8OAvK3YTHCfR)
- 度盘：地址 `s/10uTA5L5Nay1aKpqkvACM-A`，口令 `f08f`
- 115：地址 `s/sw3u78i3ze9` ，口令 `p254`
- 天翼云网盘：地址 [https://cloud.189.cn/t/Ef2IjyuuemIn](https://cloud.189.cn/t/Ef2IjyuuemIn)，口令：`jj8t`

MD5SUM：66275d47779d68614232a3e5d524af4a

永久地址（防止上面失效），欢迎关注绝版游戏保护工程：

https://github.com/skywind3000/preserve-cd


