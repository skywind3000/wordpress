---
uuid: 2852
title: CD2：SharpDevelop
status: publish
categories: 未分类
tags: 神兵利器
date: 2023-09-21
slug: 
---
SharpDevelop 是 .Net Framework 时代最受欢迎的轻量级 IDE，它代替庞大的 Visual Studio使用 C# / VB.Net 开发各种 .Net Framwork 4.5 之前的程序（WinForm，控制台，WPF，组件程序），而本身大小却只有 20MB，且运行比 VS 流畅，深受大家喜欢：

![](https://skywind3000.github.io/images/blog/2023/sharp/sharp1.png)

虽然只有 20MB 却包含完整的可视化设计器可以拖拽控件，.Net Framework 4.5 虽然不够现代，但是确是 .Net Core 前较新的一个版本，语言方面支持到 C# 5.0（包含 async/await 那个版本），并且操作系统兼容性很好，能从 Windows XP 一路兼容到 Windows 11。

本光盘兼具收藏价值和实用价值，包含了 SharpDevelop IDE 本身和多个版本的 .Net Framework 运行时环境，以及相关配套资源，当你想开发一两个小工具和轻量级的桌面应用时，无需下载安装庞大的 Visual Studio，小巧的 SharpDevelop 就能帮你迅速搞定。

SharpDevelop 被人喜爱除了免费开源外，还有个重要原因，就是启动快，运行丝滑流畅，根本不会像 VS 那样时不时卡一下，这为其赢得了不少用户。

（点击 more/continue 继续）

<!--more-->

#### 光盘目录

| 文件夹 | 内 容 |
|-|-|
| DotNetSDK | .Net Framework 3.5，4.0 和 4.5 的安装文件 |
| SharpDevelop | SharpDevelop 4 （兼容 XP）和 5（兼容 Win7+）按需选择 |
| 电子书 | C# 和 .Net Framework 的相关电子书 |
| 开发资源 | C# 语言参考手册，类库参考手册，SkinSDK，图标库等 |

#### 版本兼容

| 版 本 | C# 语言版本 | 最低操作系统版本 |
|-|-|-|
| .Net Framework 2.0 | C# 2.0 | Windows XP |
| .Net Framework 3.5 | C# 3.0 | Windows XP |
| .Net Framework 4.0 | C# 4.0 | Windows XP SP3 |
| .Net Framework 4.5 | C# 5.0 | Windows 7 SP1 |

光盘 DotNetSDK 目录内包含：dotnetfx35，dotnetfx40，dotnetfx45 几个文件，对应各个版本的安装程序，其中 dotnetfx35 安装程序同时包含了 .Net 2.0 和 3.0 的版本。对于今天的 Windows 10 一般是默认自带 1.0/2.0/4.0 三个版本的 .Net Framework，后续更新会更新到 4.8 版本（兼容 4.5）。

因此想要最大兼容性，一般可以在 SharpDevelop 里选择创建 .Net Framework 4.0 的项目，而想要新一点的语言特性（如 async/await），可以选择 .Net Framework 4.5 项目。

#### 老版本项目

唯一需要注意的是如果你想开发比较老的 .Net Framework 2.0 项目，需要在左边文件树那里，右键点击项目节点，然后菜单里选 Properties，再右侧弹出的内容里选择 Compiling 标签，并在下面 Target Framework 那里选择 Change 按钮：

![](https://skywind3000.github.io/images/blog/2023/sharp/sharp2.jpg)

把对于的 C# 版本改为 2.0 然后选 Convert 即可。

#### 开发资源

忘记 C# 怎么写了？没关系，电子书籍里有经典的 C# 入门书籍帮助你：

![](https://skywind3000.github.io/images/blog/2023/sharp/sharp3.jpg)

同时开发资源目录下面还有各种语言知识库和 MSDN 的 Reference 可以帮助你迅速查询 C# / WinForm 开发的方方面面，无需在网上翻来翻去：

![](https://skywind3000.github.io/images/blog/2023/sharp/sharp4.jpg)

MSDN 的类库速查：

![](https://skywind3000.github.io/images/blog/2023/sharp/sharp5.jpg)

能够帮助你在完全断网的情况下，迅速恢复开发。

#### 皮肤系统

本光盘包含三套 .Net Framework 时代著名的换肤系统：IrisSkin、DotNetSkin 和 SkinSharp，

可以无缝集成到 SharpDevelop 实现一键换肤，同时包含大量皮肤文件和皮肤制作工具，满足你的定制需求，帮助你迅速开发出各种风格的传统桌面软件：

皮肤样式1：

![](https://skywind3000.github.io/images/blog/2023/sharp/sharp6.png)

皮肤样式2：

![](https://skywind3000.github.io/images/blog/2023/sharp/sharp7.jpg)


#### 图标资源

有了帮助文档，有了皮肤库，要真正开始写桌面软件还需要什么呢？没错，图标库：

![](https://skywind3000.github.io/images/blog/2023/sharp/sharp8.jpg)

几大图标类别，基本够做一些常用软件了，还不满足可以下载包含十万图标的 Pichon。

#### 赠品

随光盘包含一款轻量级的 C# 开发工具：[RoslynPad](https://github.com/roslynpad/roslynpad)，它使用 Roslyn 和 AvalonEdit 技术开发，可以运行在 Windows / Mac / Linux 下面，提供一个轻量级的现代化 C# 开发环境：

![](https://skywind3000.github.io/images/blog/2023/sharp/sharp9.jpg)

让你轻松的尝试现代 C# 开发的乐趣。

#### 下载地址

度盘：地址 `s/1XKChe9EgO2RBFoT4I3zQmA`，口令 `x9gi`
115：地址 `s/swzraac3ze9`，口令 `8866`
谷歌：[SharpDevelop](https://drive.google.com/drive/folders/1V9TQORJsWHolTdPb4PtICT8GmfJldheG?usp=sharing)

为防止机器人扫描，度盘地址前面请自己添加 https://pan.baidu.com 即可，115 同理。



永久下载地址（如果上面失效），欢迎关注绝版软件保护工程：

https://github.com/skywind3000/preserve-iso


往期回顾：

- [CD1：Borland 宝典](/blog/archives/2607)
- [CD2：SharpDevelop](/blog/archives/2852)
- [CD3：Flash 开发宝典](/blog/archives/2854)
- [CD4：WinXP 开发宝典](/blog/archives/2808)


