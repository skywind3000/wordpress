---
uuid: 2808
title: CD4：Windows XP 开发宝典
status: publish
categories: 未分类
tags: 神兵利器
slug: 
date: 2024-09-02 23:05
---
今天互联网上的内容，由于各种原因，正在以越来越快的速度消失，而习惯什么都从网上找的新一代网民们，却并没有备份和记录的习惯及意识。不远的将来，会有一天，当你特别想找某个工具却搜尽互联网你都找不到时，才会发现对珍贵资源做好收藏的必要性。 

Windows XP 依然是一个完美的怀旧平台，它可以向后兼容到 Windows 95 的程序，是一个运行经典软件，玩经典游戏的完美方案。

图形界大佬 John Carmack 在推特上呼吁大家，现在应该有意识的保存你的开发环境，这样多年以后你想重新构建你的软件时才不会慌脚乱手，因为通常每过几年你常常会发现，自己之前的老代码已经没有合适的环境编译了：

![](https://skywind3000.github.io/images/blog/2024/xp/carmack.png)

本光盘包含了构建 Windows XP 程序所需要的必要工具，包括编译器，文本编辑器，集成开发环境和各种工具，他们全都能运行于 XP 下，并且能构建兼容 Windows XP 的项目。

制作原则：精选工具，断网可用，末日恢复，自包含无依赖，开发工具博物馆，帮你完全在 Windows XP 下工作，让你拥有 XP 下的沉浸式开发体验，容量却不超过一张 CD。 

版权声明：本光碟采用 [winworldpc.com](https://winworldpc.com) 类似的[版权声明](https://winworldpc.com/copyright)，尽量收录开源或者不再销售的软件产品，目的是保护这些快绝版的资源。

光盘目录如下：

![](https://skywind3000.github.io/images/blog/2024/xp/tab_content.png)

具体内容和下载地址见下文说明。

（点击 more 继续）

<!--more-->

#### 编译器（Compiler）

编译器的 Compiler 目录内包含以下几个工具：

![](https://skywind3000.github.io/images/blog/2024/xp/xp_compiler.png)

目录内包含三套 MinGW 环境，分别是 mingw-2007，msys32-xp 和 w64devkit-xp三者都大有来头，详细介绍可以看同名的 txt 文件。

首先是 mingw-2007 这个压缩包，这是 MAME 模拟器开发网站 mamedev.org 在 2008 年发布的自用工具链，包含 gcc 4.2.1+3.4.5 和 nasm / gdb 等工具，同时自带 SDL1, lua, libcairo, freetype, libjpeg, libpng, zlib, ogg 等常用库，虽然只有 24 MB，但编译 2010 年以前的老项目，老游戏非常好用。

编译单个源文件的话，直接调用里面 bin 目录的 gcc 可执行编译就行了，多文件项目的话可以用里面的 mingw32-make ，是 GNU Make 的 MinGW 版本，也可用光盘里的 cmake 生成 “MinGW Makefiles”，然后用 mingw32-make 构建。

接下来是本光盘的重头戏：msys32-xp，如果你想要一套 XP 末期的比较完善的开发工具，那非它莫属了，展开后有一套完整的 msys32 环境和一套 MinGW32 环境，内含两套 gcc 5.3.0（支持 C++ 14），一套在 /usr/bin 下面用于编译 msys32 的工具（不能脱离 msys32 环境运行）；另一套位于 /mingw32/bin 目录，用于编译正儿八经的 Windows 应用。

对比上面的 mingw-2007，这个 msys32-xp 不但包含更新的 MinGW32 环境，同时还有 msys32 环境，使得它可以用于构建基于 autotools / configure 的项目，如 SDL1，ffmpeg 等，传统大型项目不少都是需要 autotools 构建，那么光 MinGW 环境是搞不定的，还需要 msys 环境。它之所以包体达到 255MB，除了 msys外还包含大量基础库：

| 分 类 | 包名称 |
|------|--------------------------------------------|
| 图形库 | Allegro，SDL1，SDL2 |
| 网络库 | libevent，libuv，libcurl，libssh2 |
| 图象库 | libgif，libpng，libjpeg，png16，turbojpeg，webp |
| 音视频 | FLAC，mpg123，mp3lame，opus，speex，ogg，libmad |
| 压缩解压 | liblzma，zlib，libbz2，lzo2 |
| 数学计算 | gmp，fftw3 |
| 加解密 | libgnutls，openssl |
| 文字处理 | libcharset，iconv，libregex |
| CLI | pdcurses，ncurses，libmenu，libpanel |
| GUI | wxWidgets , wxPython |
| 单元测试 | gtest，cmocka，cppunit |
| 其他库 | python，ffi，jsoncpp |


新的编译器搭配的平台 SDK 经常无法编译老项目，比如用最新 msys32+mingw32 以及配套的平台 SDK 编译 cmake-3.15 时，发现 execvp 函数的第二个参数指针类型已经不兼容了，平台 SDK 尚且如此，第三方库的接口前后兼容更是堪忧，因此 msys32-xp 里各个第三方库，基本都是选择了当年版本，避免新版本接口改变，无法直接编译老代码的尴尬。

由此可见，本光盘在制作和选择开发工具上，是十分严肃认真的，不是随便扔一个光秃秃的编译器给你，更不是给你一堆最新的库，根本无法编译老项目。

这个 msys32-xp 开发环境可以直接编译一些经典游戏，比如Yamagi 的 Quick II for Windows XP 等，所有依赖都包含在内了，并且版本契合。同时还配套一些实用工具，如：Python，tmux，lua，git，ssh，lftp，curl/wget，vim，nano，cmake，gdb 等，基本上是一个自成一体的小型独立完整开的发环境了，就算不依赖本光盘其它工具，它也能自我闭环。

第三套 MinGW 环境是 w64devkit，他是今天还在维护着的最新项目，主页在这里。该项目刻意保持对 XP 的兼容性（虽然名字里有个 64 却兼容 32 位 XP），内部包括 gcc 14.2 + gdb 和一套基于 busybox 的 shell 环境，你能用它在 XP 下面写 C++ 23 的代码，也能用 mingw32-make / cmake 来搭配构建项目，但无法编译基于 autotools 的东西。

![](https://skywind3000.github.io/images/blog/2024/xp/tab_mingw.png)

其实 GCC 版本较新的 w64devkit 也可以同 msys 搭配编译 autotools，做法就是在 msys32-xp 解压后，进去建立个 mingw64 目录，然后把 w64devkit 压缩包解压进去，再到 bin 目录里把 busybox 导出的可执行全删除了（就是 sed/bash 那些 4KB 的），然后用 shell_mingw64.bat 进入环境，虽然叫 64，编出来还是 32 的。

也能在 msys 环境里用 mount 命令把他们临时 mount 到 /mingw32 或者 /mingw64，或者写 /etc/fstab 固化下来，而不用改动 msys32-xp 内原有目录。

最后是 Visual C++ 9.0 的命令行编译工具，对应 Visual Studio 2008，可以用来编译一些经典 VC 项目，我记得 Python 官网推荐的，他们用这个构建 Python2.7 的，使用的话在命令行运行 vcvarsall.bat 初始化环境，然后就可以使用 cl.exe / link.exe 之类的工具了，也可以用 cmake 来生成 “NMake Makefiles”，然后调用 nmake 构建项目。

本光盘主题是 XP 开发工具，那编译器自然是最重要的东西，但搭建一套真能用的 XP 开发环境，光有编译器也不够，还得有其它工具搭配使用。

#### 文本编辑器（Editor）

编辑器目录内包含多款能运行于 XP 的经典编辑器，比如用来写程序编辑网页的 UltraEdit32：

![](https://skywind3000.github.io/images/blog/2024/xp/xp_ultraedit32.png)

体积小，功能强，速度快的编辑器（1.9MB），可以用来开发写代码，可以配置编译器，捕获编译错误，可以比较文件，可以做二进制编辑器，当年很流行，关于如何配置编译器，如何一键运行程序，在 UltraEdit32.txt有详细说明，一看便知。

在 XP 时代同 UltraEdit32 齐名的编辑器还有两个：EditPlus 和 NotePad++，其中 EditPlus 同样是一款小巧轻便的编辑器：

![](https://skywind3000.github.io/images/blog/2024/xp/xp_editplus.png)

它能多 TAB 打开文档，提供文件树，能够配置外部工具，集成编译器，并且捕获编译错误，还能显示文件大纲和函数列表，打开远程文件；光盘内收录了最后一个可运行于 XP 的 EditPlus 4.30，关键它启动速度快，打开文件快，而包大小才 1.9MB。

三剑客最后就是 NotePad++ 了，版本选的 7.9.2，最后一个支持 XP 的版本（2021）：

![](https://skywind3000.github.io/images/blog/2024/xp/xp_npp.png)

NotePad++ 是一款支持插件的编辑器，作为一张负责任的光碟，保证断网可用，末日恢复，自然不会光收录一个编辑器本体，几个核心插件自然也做成压缩包了：

![](https://skywind3000.github.io/images/blog/2024/xp/xp_npp_plugin.png)

把他们解压到 NotePad++ 的 plugins 目录就能使用，简单介绍下：

- Explorer：左边显示文件树面板，收藏面板。
- FileSwitcher：使用 Ctrl+Shift+o 快速切换文件。
- NppExec：执行外部命令，常用于配置编译器到 Notepad++，并在下方显示编译错误。
- NppAutoIndent：更智能的缩进。
- NppEditorConfig：加载 EditorConfig 配置。
- LuaScript：使用 Lua 增强 Notepad++ 功能。

这几个插件能让 NotePad++ 的易用性增加不少，属于必备插件。比较幸运的是除了 LuaScript 外，其它的最新版都能在 XP 下直接使用，所以本雷锋选择了最后一个能运行于 XP 的 LuaScript 版本，同时附带一个 launch.cmd 可以用于 NotePad++ 里 Ctrl+F5 运行各种各样不同的程序，用法见 “使用说明.txt” 。

这三款编辑器基本是 XP 时代最出名的文本编辑器了，选择一款你喜欢的，搭配前面的编译器，基本可以开始干活了。

喜欢 vim 的人，会发现目录里有 vim-9.0.0494，这是 2022 年底的版本，能在 XP 上用到 Vim 9.0 是一件很难得的事情；安装包会同时安装桌面版的 GVim.exe 和命令行版vim.exe，满足不同用途：

![](https://skywind3000.github.io/images/blog/2024/xp/xp_vim9.png)

光有 vim 没配置也不好用，因此同目录中包含了一份我自己的离线配置和一些辅助工具，包括把用 vim 的新 tab 打开文件添加到右键菜单，交换 ctrl/caplock 的注册表文件等。

想要完全在 XP 下沉浸式工作，那么除了编写代码外，经常做的事情是什么呢？对，还需要大量阅读代码，那 XP 下读代码最好用的工具就非 Source Insight 莫属了：

![](https://skywind3000.github.io/images/blog/2024/xp/xp_si.png)

这不是那种 2009 年的古董 Source Insight，而是 2019 年的版本，是 XP 在 2014 年生命终结五年后还在继续更新的版本，当然，也是最后一个能用于 XP 的 Source Insight 了。

有时在命令行下面工作，偶尔改两行配置又懒得打开 GUI 编辑器，这时命令行下的编辑器就有用武之地了，除了之前 vim 9 的命令行版本外，还收录了 nano-7.2 和只有 62KB 的 zvi （最小 vi 克隆），二者既可以运行于控制台，还能运行于 ssh/telnet 连接的远程终端，可以保存到你的 U 盘里面，极端情况下江湖救急。

编辑器目录内还有其它几款有意思的文本编辑器，欢迎自行探索。

#### 集成开发环境（IDE）

首先是经典工具 Visual Studio 6.0 ，允许你编译一些更为古老的项目，XP 的兼容可以向后追溯到 Windows 95，基本上非常古老的程序都能在 XP 上运行，这也让 XP 成为了一个完美的怀旧平台，那么如果你想重新构建这些古老的项目，那 VC6 基本是绕不开的：

![](https://skywind3000.github.io/images/blog/2024/xp/xp_vc_1.png)

这个虽然是一个 VC6 的精简版，但核心工具一件不少（命令行构建工具，GUI 工具，ERRLOOK，DEPENDS 等），核心组件也样样齐全（MFC/CRT 包含代码），并且包含 SP6 补丁，为了让大家能够高效的在 VC6 环境下工作，这个版本还附带了几款广受好评的插件，比如 VAX 和 WndTab，都是当年的版本，现在想找恐怕都很难找到。

安装的话很简单，参考压缩包里的 “使用说明.txt”，比如以 VAX 为例，去到 plugins 目录内的 VAX 目录，运行 Reg.bat 进行注册，重启 MSDEV.EXE 就行了：

![](https://skywind3000.github.io/images/blog/2024/xp/xp_vc_2.png)

红番茄（VAX）安装完毕，进去后工具栏多了一行红番茄的专属按钮：

![](https://skywind3000.github.io/images/blog/2024/xp/xp_vc_3.png)

可以支持文件快速切换（Alt+Shift+o），符号查找，补全增强，代码片段等现代 IDE 功能，让 VC6变得更顺手；不想用的话随时运行 UnReg.bat 注销。

其它 VC6 相关工具和插件可以自行探索压缩包，不要忘记阅读里面的 “使用说明.txt”。

觉得 Visual Studio 6.0 太老了没关系，光盘 IDE 目录内另一个软件，就是 Orwell 版本的 Dev-C++ 5.11，这是最后一个正统的 Dev-C++ 了，后面就由 Embarcadero 公司（目前 Delphi / Rad Studio 那家母公司）接手了：

![](https://skywind3000.github.io/images/blog/2024/xp/xp_devc.png)

默认配套的工具链是 TDM-GCC 4.9，支持 C++ 11，同时允许你添加其它工具链，比如你可以添加之前 Compiler 目录内的其它 MinGW 工具来编译，除了不能像 VC6 一样写 MFC 画对话框，其它 Win32 / Console 程序都支持。

而如果有一些界面小工具要开发又不想写 Win32/MFC 怎么办呢？试试 SharpDevelop：

![](https://skywind3000.github.io/images/blog/2024/xp/xp_sharp1.png)

SharpDevelop 是 .Net Framework 时代最受欢迎的轻量级 IDE，它代替庞大的 Visual Studio使用 C# / VB.Net 开发各种 .Net Framwork 的应用程序（WinForm，控制台，WPF，组件程序），而本身大小却不到 20MB，且运行比 VS 流畅，深受大家喜欢。

而 SharpDevelop 4.4 是最后一个支持 XP 的版本，XP 原版支持 .NET Framework 3.5，而 XP SP3 支持 .NET Framework 4.0，在 SharpDevelop 里创建新项目时可以选择：

![](https://skywind3000.github.io/images/blog/2024/xp/xp_sharp2.png)

默认直接上 4.0 即可；目前本光盘提供了几套开发 GUI 界面程序的方式：

- Win 32 裸写：所有工具都支持；
- MFC：用 Visual Studio 6.0 才行；
- wxWidgets：用 msys32-xp 里的 MinGW 环境。
- wxPython：用 msys32-xp 里 MinGW 里的 python 开发。
- WinForm：用 SharpDevelop + C# 开发。

应该满足大部分 GUI 开发需求了，目前 IDE 目录内三套软件，每套软件本雷锋都附了文本文件，包含用法说明：

![](https://skywind3000.github.io/images/blog/2024/xp/xp_ide.png)

都是经典版本，兼具收藏和使用价值。

#### 工具目录（Tools）

光盘的 Tools 目录内容如下：

![](https://skywind3000.github.io/images/blog/2024/xp/xp_tools.png)

光盘内有很多压缩包，为了保证断网可用，自然包含了两个解压软件：7z2408（这是 24 年8月份的最新版本），和 WinRAR 6.0（最后可用于 XP 的版本），即便你在一台全新的 XP 机器上也可以无依赖的解压光盘内其它内容。

系统工具有 DTLite4356，即 XP 下面经典的虚拟光驱软件 DAEMON Tools 的 Lite 版本，这样本光盘如果以 iso 形式传递也能在 XP 下直接打开；还有一个是 MenuMgr1.2.exe，可以用来清理鼠标右键菜单的；还有一个工具是 ProcExp，没错就是那个好用的任务管理器，最新版居然支持还 XP，那直接收录。

开发方面的工具自然包括 cmake-3.13.5（3.14 就放弃 XP 了），解压后把 bin 目录添加到PATH 环境变量就能使用；先前的 msys32-xp 的 /mingw32/bin 下的 cmake 版本只有 3.2，想搭配使用这个的话把 cmake 的 bin 添加到 PATH 最前面，先于 /mingw32/bin 就行；最后还有个构建工具 emake，采用类似 IDE 的定义式构建方式，非命令式，中小项目非常方便，欢迎尝试。

我写程序喜欢 log 调试，但是 Windows 下缺乏一个好用的日志实时查看工具，于是我收录了三个比较小巧的工具：TailW32，baretail 和 mtail，从简单到复杂，第一个重在体积超小，左边有文件列表方便切换；第二个特点是多 tab 日志同时打开监控，关键字上色；第三个是功能最强的，还有报警功能。

其它的 DEPENDS.EXE 用于查看可执行和动态库的依赖关系，ERRLOOK.EXE 用于查询 Windows 错误码的文字含义，都是 Windows 下开发经常使用的工具，这两个虽然都来自 VC6 的安装盘，但比最新版好用很多，最新版 DEPENDS.EXE 碰到复杂的依赖关系或者循环依赖关系会计算半天，有时还会界面卡死不动，远不如光盘里的版本好用。

最后是我个人多年的珍藏，自己不断整理维护的工具包，也是工具目录压箱底的东西：

![](https://skywind3000.github.io/images/blog/2024/xp/gnu-tools.png)

这是我个人多年整理的 gnu-tools-xp.rar 工具包，别看它只有 4.5MB，内容却毫不含糊：

![](https://skywind3000.github.io/images/blog/2024/xp/busybox2.png)

相信很多人都用过 busybox，这是 Win32 版本的，内部包含 172 个 unix 工具：

![](https://skywind3000.github.io/images/blog/2024/xp/busybox.png)

用法就是：“`busybox <工具名> [参数]`” ，比如要调用里面的 ls 工具查看目录：

```bash
busybox ls -la
```

它就能像 linux 下的 “`ls -la`” 命令一样，按 ls 的格式列出当前目录下面的文件，这个版本的 busybox 基本包含了所有 GNU 必备工具了，其中一些较为复杂的有：

- ash：busybox 版本的一款 shell，基于 ash。
- awk：用于模式匹配和文本处理的一门脚本语言。
- sed：流式文本编辑器，多用于自动批处理修改文本。
- vi：很强大的文本模式可视化编辑器，能运行于远程终端，这里有[一份教程](http://k.japko.eu/busybox-vi-tutorial.html)。

基本上一个 busybox 就能搞定所有在 Windows下运行 GNU Tools的需求，更多使用帮助可以访问它的项目主页：https://frippery.org/busybox/ 。

这个 gnu-tools.rar 压缩包里有不少独家的东西，比如 cscope.exe，搭配 vim 可以把 vim 变成一个 C 语言的 source insight，它可以分析项目代码，建立数据库，然后帮你查找符号的定义和引用，网上下得到的是 15.8a 的 Windows 可执行，但作者后来发布过一个 15.8b 的修正版，改了不少 bug，不过不能运行于 Windows，本雷锋花了两天移植，这是全网最新的Windows 版本。

另一个代码分析工具 ctags.exe 也是众多编辑器里必备的工具，用于 Vim 里显示当前文档的函数列表，用于定义查找和跳转，支持 65 种编程语言，用的最新的 universal-ctags，官网的可执行早已不能运行于 XP，这是我幸苦找到的一个版本。

接下来是 edlin，这是 DOS 时代官配的行文本编辑器，原版本已经无法运行于后来的 Windows 系统了，这个是后来由 Gregory Pietsch 移植的 Win32 版，同样支持 XP；当然，虽然没啥实用价值，但有收藏和怀旧的价值。

接下来是著名的终端文本编辑器 nano：

![](https://skywind3000.github.io/images/blog/2024/xp/nano1.png)

这个编辑器历史悠久，先祖可以追溯到 unix 下的 pico 编辑器，遗憾的是早在 N 年前的 nano-4.9 时就放弃了对 Windows XP 的支持，本着不抛弃不放弃的原则，本雷锋 backport 了 2024 年夏季的最新版 nano-7.2，它不但能运行于 Win XP -> Win 11 的所有命令行，还能运行于远程终端，当你用 ssh/telnet 连接一台 Windows Server 或者 Server Container 时，可以在远程终端里运行它。

另一个 zvi 编辑器同 nano 类似，一样运行于 Win XP -> Win 11 所有系统的命令行，同样支持远程终端和无桌面的 Server Container，这是 busybox 里面的 vi 编辑器，被我扣出来作为独立可执行了，满足 vim 用户的使用习惯，大小只有 62KB，可谓最小 vi 了：

欢迎关注项目主页：https://github.com/skywind3000/zvi 。

放两张截图，运行于 Windows XP 下：

![](https://skywind3000.github.io/images/p/zvi/zvi_xp.png)

使用 PuTTY 连接 Windows Server 运行 zvi 于远程终端中：

![](https://skywind3000.github.io/images/p/zvi/zvi_ssh.png)

可以把这个 zvi（62KB）和前面的 nano（87KB）放到你的 u 盘里，关键时候进行救急用。

#### 版本控制工具（VCS）

既然要搭建正儿八经的开发环境，版本管理工具自然不能少：
 
![](https://skywind3000.github.io/images/blog/2024/xp/vcs.png)

有独立的 Git 工具，也有 TortoiseGit，我听说不少游戏公司现在还在用 SVN，所以放了个  TortoiseSVN（包含命令行 svn），都是最后能够支持 Windows XP 的版本。

#### 脚本语言（Script）

光盘的 Script 目录中包含了 Python 和 Lua 的新老版本：

![](https://skywind3000.github.io/images/blog/2024/xp/dir_script.png)

XP 下面任然有不少程序是用脚本语言开发的，有些还会用到老版本的解释器，比如有很多 Python2 的老代码，因此这里同时包含了 Python-2.7 和 Python-3.4.4（最后一个兼容 XP 的 Python），兼顾老代码与新代码。

同样 Lua 的选择上也在包含了传统经典版本 5.1 的同时收录了最新的 5.4.7，都包含了二进制可执行和源代码。

#### 网络工具（Network）

当你需要进行远程开发，登陆远程服务器时，少不了终端软件：

![](https://skywind3000.github.io/images/blog/2024/xp/dir_network.png)

这里有 2024 年最新的 putty-0.81（感谢 putty，多年一直保持 XP 的兼容性，让我们现在都能在 XP 下用到最新版），还有很多人喜爱的 MobaXterm 绿色版。

附带了个迅雷精简版，我珍藏的一个版本，体积小界面清爽：

![](https://skywind3000.github.io/images/blog/2024/xp/minithunder.png)

另外还有其它几个经典小工具，欢迎自行探索。

#### 媒体相关（Media）

光盘的 Media 目录下包含如下软件：

![](https://skywind3000.github.io/images/blog/2024/xp/dir_media.png)

本光碟制作原则就是考虑完全在 XP 下工作的情况，那么开发除了写代码，当然需要读文档，因此收录了 FoxitReader 早年的一个绿色单文件版本（非自解压版）：

![](https://skywind3000.github.io/images/blog/2024/xp/foxitxp.png)

不是那种自解压程序，每次运行需要生成一堆临时文件，就是纯的绿色单文件，仅 5MB。

另外还有 ACDSEE 最经典的一个版本 2.44，任然是绿色单文件，方便查看老游戏的资源文件。为了提升工作时的专注力，有时候写着代码看着文档想听点音乐怎么办呢？ 

![](https://skywind3000.github.io/images/blog/2024/xp/winamp.png)

请出我们的老朋友：Winamp，版本选择的是 5.6 Lite 版本，XP 下面听音乐的最佳搭档；听说他们最佳还出了一个最后的版本 5.80-build-3660，我试了一下，没法再 XP 下安装了，因此这个 5.6 Lite 应该是 XP 下最后的 Winamp 了。

最后还有个 FlashPlayer 14.0，可以播放大部分怀旧 Flash 动画，可以玩大部分 Flash 游戏（Flash 游戏主要是集中在 9-14 版本号），兼容性最好。

到此为止《XP 开发工具》这张 CD 的内容基本制作完成了，最后发布前我突然在想，前面的内容都太严肃了，是不是放几个轻松的小游戏调剂下？免得程序员等待编译时无聊，于是增加了一个 “赠品” 目录：

![](https://skywind3000.github.io/images/blog/2024/xp/dir_gift.png)

都是一些经典的小游戏，直接运行无需安装，其中有汪海涛的《潜艇大战》，是个 MFC 程序，玩家控制军舰左右移动，用深水炸弹炸潜艇：

![](https://skywind3000.github.io/images/blog/2024/xp/submarine.png)

别看这个 “潜艇大战.EXE” 文件只有 404KB，当年学生时候我却玩的不亦乐乎，几次重装电脑都舍不得删除，一直保留到现在，今天玩起来依然很有意思，十分解压。

另外几个都是精挑细选的经典 Flash 游戏，可以用 Media 目录里的 FlashPlayer 14 来播放，最好拷贝到 C:\Program Files 然后设置下 .swf 文件默认由它来打开，然后就能双击运行：

![](https://skywind3000.github.io/images/blog/2024/xp/flash1.jpg)

觉得潜艇游戏节奏快可以试试这款比较休闲的麻将，制作很精良，全程语音；有了这几个小游戏在这里，等编译时再也不会无聊了，即便没网络，也可以放松一下，换换脑子。


#### 网络资源

本光盘最开始我准备了两张光盘的内容，然后精挑细选，反复比较，留下了最精华的一张光盘内容，这么多东西，总体 ISO 大小只有 649MB，小于一张 CDR 的容量。

选择制作成 650MB 以内的 ISO，一方面是便于收藏和分享，另一方面是强迫自己有所取舍，留下真正精品的东西；虽然，还是有一些我觉得很有意思的东西没机会收录，所以我在 github 上新建了一个叫做 abandonware 的网站，把他们做成额外 DLC 陆续放上去。

本光盘的 DLC 专用网址：

- https://github.com/skywind3000/abandonware/releases/tag/0.0.1 

最后是一些 Windows 开发用得上的资源：

- [Win32 Help File （CHM）](https://web.archive.org/web/20220922051031/http:/www.laurencejackson.com/win32/)
- [Intel Intrinsics Guide（交互式汇编指令集帮助）](https://www.intel.com/content/www/us/en/docs/intrinsics-guide/index.html)
- [Windows-XP-Stuffz（XP 常用工具）](https://github.com/Alex313031/Windows-XP-Stuffz)
- [w64devkit （最新的支持 XP 的开发环境）](https://github.com/skeeto/w64devkit)


#### 下载地址

光盘下载：

- 谷歌：[WindowsXP-Devkit](https://drive.google.com/drive/folders/1yJ8otnpKMhbrDmNUei0_WFGbNaeU6Yea?usp=drive_link)
- 度盘：地址 `s/1fWWskQYbbk0Eemp3eSFU2Q`，口令 `z8gd`
- 115：地址 `s/swh3bpl3ze9`，口令 `8866`
- MD5SUM： fcdd640440bfbf0304338a8c70d7bea4

避免机器人扫描，读盘地址前请自己拼接 `https://pan.baidu.com/` ，115 自行添加 `https://115.com/` 即可。

《绝版软件保护工程》永久地址：

- https://github.com/skywind3000/preserve-iso 

更多信息，类似光盘请访问上述官网。

往期回顾：

- [CD1：Borland 宝典](/blog/archives/2607)
- [CD2：SharpDevelop](/blog/archives/2852)
- [CD3：Flash 开发宝典](/blog/archives/2854)
- [CD4：WinXP 开发宝典](/blog/archives/2808)

