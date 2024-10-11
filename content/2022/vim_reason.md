---
uuid: 2970
title: 我为什么使用 Vim？
status: publish
categories: 随笔
tags: Vim
slug: 
date: 2022-08-26 17:20
---
很多人说用 Vim 是因为键位比较方便，其实这只是部分原因，不知道你思考过没，为什么今天大部分 Editor/IDE 都支持 vim keymap 的情况下，还有那么多人用 Vim 呢？如果仅仅因为键位原因，他们大可以用其他东西啊，为何还继续用原始的 Vim 呢？

也许在你看来，有的人配置 Vim 一半天最后就是类似 IDE/Vscode 的样子，既然如此，那么为啥那些人不直接去用 IDE/Vscode 呢？（二者也都支持 vim keymap），为什么他们还抱着原版的 Vim 不放呢？难道真的是他们没听过/没用过时下最先进的 Editor/IDE 么？

事实可能恰恰相反，很多 vimer 都是非常热衷尝试各种新的编辑器的，我给 vscode 写过不少高赞回答，也给 atom editor 开发过插件，不少 vimer 机器上 terminal/gui based 的 editor 加起来都有十多个，对主流 editor/ide 的熟悉程度未必比非 vimer 差。

那么究竟为啥还有人用 vim 呢？CoC 作者赵启明老兄已经回答了："Vim 大概是世界上扩展能力最强的编辑器"。Vim 就像编辑器世界里的 MineCraft，你说 MineCraft 最终目标也就是去杀条龙，为什么那么多人不直接玩也能杀龙的黑魂/老头环，却一直迷恋 MineCraft 呢？

因为 MineCraft 每一寸土地都可以定制化，每种游戏元素都可以自己制作（除了工具武器制作外还可以制作各种玩法的副本关卡，还有人用 MC 里的红石从门电路做起，搭了个 CPU），而 Vim 里每个字符你都可以定制。

方便定制体现在两个方面：首先是能定制的地方很多，到处都能改（不像 vscode 一样对插件开发者诸多限制，连个 toolbar 按钮你想加都加不了）；其次是非常容易上手修改，改的代价非常低，不用加个简单功能都要创建个插件项目，编辑 package 配置等一堆七七八八的文件，一半天才能开始写一行代码。

我用过非常多的编辑器，有一些至今我都非常喜欢，但不管我多么喜欢一款编辑器，总有一些地方是我不满意的，碰到这种时候，大部分我只能祈求开发商发慈悲哪天给我加一下，即便有些开源的，支持扩展的，很多都没达到 Vim 的扩展性，可以那么容易的让普通用户随心定制，四处定制。

用其他 Editor/IDE 的用户大部分都是下下扩展，改下按键之类的，而 vim 用过一年以上的几乎人人都可以随手扩展，举几个例子：

<!--more-->

#### 例子1：格式化代码

比如我看 html 的时候有时候很混乱，需要格式化一下，我知道有专业的格式化软件，懒得费时间找了，直接几行 vimscript 搞定：

```text
function! Html_Prettify()
	if &ft != 'html'
		echo "not a html file"
		return
	endif
	silent! exec "s/<[^>]*>/\r&\r/g"
	silent! exec "g/^$/d"
	exec "normal ggVG="
endfunction
```

随手一段小代码，然后配置给 F12，碰到 html 直接 F12 就完成格式化了，根本不用费力找工具。

（Vim 里有各种专业格式化插件，包括基于语义的，能理解代码的格式化工具，我只是演示下扩展能力，简单需求不用找，三分钟解决）。

再比如说我写 C++ 时，最痛苦的就是头文件里写了一堆类成员函数定义，把他们拷贝到 .cpp 文件里，还要把诸如：

```cpp
void translate(float x, float y, float z) ;
void rotate(float x, float y, float z, float theta);
void scale(float fx, float fy, float fz);
```

一大堆从头文件里拷贝过来的定义整理成：

```cpp
void matrix4::translate(float x, float y, float z)
{
}
```

之类的实现，每次要再前面添加 `classname::` 后面要把分号换成 `{ ... }` 还要补一些空行，想不出任何工具可以帮我做这个事情，但 vim 里，随便写几行 vimscript，实现一条新的 vim 命令，选中要改变的代码，输入类名，瞬间就能把选中代码从第一种形态变成第二种。

这类例子太多了，每个人都会有一些自己的问题需要解决，有些有现成工具，有些没有，用 vim 的话，不管有没有三下五除二就能弄出来，比如编辑 markdown 时，从别处拷贝一个 tab 分割的表格过来，你也可以写个新的 vim 命令瞬间把他转换成 markdown 表格。

#### 例子2：功能完善

比如 vim 下曾经编译/运行 C/C++ 程序困难，我随手撸了个脚本 asyncrun.vim：

![](https://github.com/skywind3000/images/raw/master/p/asyncrun/screenshot.gif)

可以异步编译，并把结果显示在下面的窗口里并匹配错误，同时还支持多种运行方式，比如弹出一个 cmd.exe 运行，新 tab 上用内置 terminal 运行，gnome-terminal 里运行等。

#### 例子3：学习其他编辑器

其实 Vim 用户乐于尝试不同的编辑器也是在学习他们优秀的地方，比如 vscode 里前脚出了 lsp, dap ，后脚就有 vim 用户做了插件支持。

比如我看到 vscode 里的 task 功能不错，我也写了个小脚本 asynctasks.vim 来允许不同项目配置不同的任务：

![](https://skywind3000.github.io/images/p/asynctasks/demo.gif)

上图中，左边是任务配置，配置好任务，立马在 fuzzyfinder 中就可以选择到，当然也可以绑定到某个按键上，而且我做的时候还可以加入不少 vscode 里没有的功能，比如任务结束播放音效提醒，比如引入全局任务免去默认项目重复配置之苦（当时 vscode 的 task 还没有全局任务，后来他们加了）。

比如我曾经在某个收费 IDE 里（好像是 pycharm 还是啥）见过代码实时格式化，写完代码 ctrl+enter 的话就可以实时格式化当前行，我很喜欢，如果我没有 vim 就只有羡慕的份，而有了 vim 的话，根本不用羡慕，花两个小时写段小脚本就有了：

![picture](https://skywind3000.github.io/images/p/pep/rtformat_4.gif)

一模一样的功能，还不像 pycharm 那样只支持 python，它支持一堆语言。

我从 vscode 那里抄了一大堆功能到我的 vim 里了，再比如 vim 里虽然有内置终端，但是没有 vscode 那种 ctrl+' 快速切换的好用，我也抄到 vim 里了，ALT+= 快速下方打开/关闭终端窗口。

其他很多 vim 用户也同我一样抄了很多 vscode 的功能回来，但是反过来很多功能很难从 vim 里抄给 vscode，比如文本对象，到今天都是个 vscodevim 插件里的半成品。

#### 例子4：界面扩展

我在 Vim 里配置了很多 keymap，经常搞忘，我就想，能不能给 vim 加个主菜单目录啊，跟以前 Turbo C++ 一样的，于是周末我花了两天时间，加上了：（点击播放）

![](https://skywind3000.github.io/images/p/quickui/screenshot.gif)

嗯，熟悉的 turbo c 目录，但是边角不是特别好看，还是有点粗糙，我又改了一版，支持风格：

![](https://skywind3000.github.io/images/p/quickui/color2.png)

看起来还行，再调整下配色：

![](https://skywind3000.github.io/images/p/quickui/color1.png)

看起来不错。

后来我在某 Java IDE 里看到一个功能，查看函数定义时，可以不跳转，开一个小窗口就行，似乎很酷，立马移植：

![](https://skywind3000.github.io/images/p/quickui/preview_tag.png)

有了，浮窗预览函数/类的定义，光标移动或者 esc 就自动关闭。

#### 例子5：集成外部工具

Vim 可以方便的同各种外部工具集成，比如同 cppman 继承：

![](https://skywind3000.github.io/images/t/2024/vim/cppman.jpg)

左边源代码处光标在 wcslen 上弹出菜单，选择 Cppman，右边就会显示 cppman 的帮助内容，这个功能我用的很顺手，但是只支持 C/C++，于是我又加了个 dash/zeal 的支持，可以一键弹出 dash/zeal 显示光标下元素的帮助：

![](https://skywind3000.github.io/images/t/2024/vim/zeal.jpg)

光标在 python 代码的 time.sleep 处，一键打开 dash/zeal 帮助。

#### 例子6：解决实际问题

你花两天时间熟悉了 vimscript，基本上碰到问题，你都不需要向外求助，向内求自己就足够了，比如 vim 虽然有一大堆智能补全插件了，但是当我到远程服务器上临时编辑时，我并不想下载安装一大套补全系统，再编译各种 LSP 后台服务，我被这个问题困扰一段时间了。

后来就想，为什么不做个轻量级补全插件呢，只要不提供智能语义补全，仅仅支持历史+字典补全的话就会很轻松，于是花了一个周末，写了一百多行 vimscript 就搞定了：

![](https://skywind3000.github.io/images/p/auto-popmenu/demo.gif)

现在我远程编辑也能有一个简单基础的补全了，特别字典补全，写英文邮件和文档时就很有帮助，尤其是碰到不少长单词只记得住部分那种，我觉得一个周末的时间在一个小地方永久改善了我的工作效率是值得的。

也许你会觉得自己没有那么多的时间搞编辑器，其实我也没花多少时间，我大部分时候是碰到问题了，想个办法然后解决，大部分问题三分钟一段小脚本即可，偶尔复杂点花一个周末弄一下。也就是把别人玩游戏的时间拿来优化下自己的编辑器而已，关键是一次投入，持续受益。

或许你还会觉得我是 vim 高级用户，才能自己自己完善扩展编辑器，其实并非如此，不同于别的编辑器，很多一年以上经验的 vim 用户平时都有边用边扩展的习惯，而我顶多算稍微有点经验的用户，vim 水平比我高的多的是，楼下的赵启明就比我厉害多了。

例子太多了，不想举了，还是那句老话：也许 vim 是世界上扩展能力最强的编辑器。不但代表到处可以定制，同时定制的门槛都比较低，隔壁 emacs 扩展也很强，但是必须用 elisp ，再 vim 里你可以用：vimscript, python, lua, javascript, ts, racket, tcl, perl, ruby 等等一系列语言来做扩展，没有一款编辑器做到如此地步。

当然，必要的 vimscript 还是要掌握的，即便你的主要程序可以用其他语言来开发，但是程序员一辈子要学几十种语言，下面有一分 vimscript 入门教程：

[VimScript 五分钟入门（翻译）](https://skywind.me/blog/archives/2193)

#### 对编辑器有很高要求的人才会选择 Vim

随便用一下，什么编辑器都可以，大部分 vimer 最早都是用其他编辑器的，只有真正用进去，真的喜欢上某些编辑器的一些功能，同时又深深的觉得有一些不足需要改进时，你才会去思考这个问题，才会去深入思索自己真正想要的是啥。

而当你一次次试了一款又一款不同的编辑器都没找到你想要的东西时，你会意识到，这些编辑器都不是属于你的，只有 Vim 才是真正属于你自己的编辑器，只有 Vim 才能让你常用常新，也能越用越贴身，越用越顺手，其他编辑器很难做到这一点。

按玩游戏类比，他们天花版太低了，塞尔达内容再优秀，玩 200 小时也就索然无味了，根本不够我玩，但 MineCraft 玩家，玩几年还在玩的大有人在。vim 也一样，它的天花板，上不封顶，即便用了很多年你也能不停进步，持续提升效率，如果你对编辑器有很高的要求又喜欢折腾的，那么它有足够的空间让你折腾。

另一个额外收获是，不用像别人一样，学门新语言就要换一个 IDE，经验和习惯不能复用，特别当你同时开发多种语言时，这种不停切换带来的割裂感是很不舒服的，而很多最新的技术和语言才出来几年时根本没有啥 IDE，你非要等成熟 IDE 出来才肯碰，经常就晚了，用 Vim 的话不管你写几门语言，不管技术新旧，都能让你保持高水平的一致的体验。

嗯，简单回顾了一下我是怎么用 vim 的，回到开头的问题“今天大部分 Editor/IDE 都支持 vim keymap 的情况下，为什么还有那么多人用 Vim 呢？”，现在我想答案应该很清晰了。

> 不被时间和环境束缚，幸福的完全按照自己的想法和习惯编码时，一瞬间你会变得随心所欲，自由自在，这种不被任何人打扰，无所顾虑的真正享受编码的孤高行为，可以说，这才是现代程序员都平等拥有的最好的自我治愈。

PS：很多人说 Vim 老，一点不老，vim9 不是刚刚才发布的么，得益于越来越强大的扩展能力，他能随时追上时下最新科技，什么 git-lens，tabnine，copilot，配合 vim 强大的插件开发社区，其他编辑器前脚出，vim 后脚就有了。

这不，最近又有人给 lsp 插件添加了 inlay hints 类似 jetbrains 的嵌入在代码里的提示：

![](https://skywind3000.github.io/images/t/2024/vim/coc1.jpg)

可以用灰色字体（非代码，是 virtual text）提示你参数含义和变量类型，曾经 jetbrains 的绝活：

![](https://skywind3000.github.io/images/t/2024/vim/jetbrain.jpg)

如今使用 Vim9 最新提供的 virtual text 也能轻松实现了，无需花一分钱购买。

相关阅读：

[VIM这么难用，为啥这么多人热衷？](https://www.zhihu.com/question/437735833/answer/1716873219)

