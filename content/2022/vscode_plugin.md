---
uuid: 3082
title: VSCode 有哪些让人眼前一亮的插件？
status: publish
categories: 随笔
tags: 神兵利器
slug: 
date: 2022-03-29 18:53
---
VSCode 里很多插件看着很好玩，但装上看一下你就不会再用了，还有些插件所有人都推过，一堆人推来推去还是那么几个，越看越无聊，因此再说这些也没什么意思，还不如直接看下载排行榜去。

我选插件就一个标准：提升工作效率！分享几个我自己用的能让生活变得更容易的插件：

1）Project Manager：

![](https://skywind3000.github.io/images/blog/2022/vscode/vsc1.png)

用 vscode 经常在项目里切换来切换去，Open Directory 效率太低，命令行 `code .` 用着也不方便，这个 Project Manager 是解决这个痛点存在的：

- 左上是项目收藏面板，点击 “软盘”图标可以收藏当前项目，下次直接点击就切换。
- 左下是项目扫描，设定几个目录，会自动扫描这几个目录下面所有 svn/git 项目，双击切换。

有了这两个面板，项目切换随心所欲，想切就切。

2）Notes

![](https://skywind3000.github.io/images/blog/2022/vscode/vsc2.png)

笔记插件，安装后，设置一个存储笔记的地方，然后该路径下的 markdown 文件会专门显示在 Notes 插件的面板里，集中管理。当然有更专业的笔记软件，这个插件的优势是就在 vscode 的侧面板里，非常容易访问到，不需要多开一个软件，不影响当前 vscode 正在打开的项目，适合随手记录一些比较零碎的东西。

尤其适合记录一些代码相关的东西，然后设置保存在 onedrive 目录里，多台电脑云同步。搭配其他 markdown 插件，可以方便的实现笔记内链（按 CTRL+鼠标左键跳转），图床之类的功能。

（点击 more/continue 继续）

<!--more-->

3）vscode-mindmap

![](https://skywind3000.github.io/images/blog/2022/vscode/vsc3.jpg)

脑图支持，项目里新建一个 .km 文件，然后用它打开，直接编辑脑图，适合在没有装 xmind 的情况下，画一些脑图，同事支持多布局，多种风格；还有一个叫做 nano mindmap 的代替品：

![](https://skywind3000.github.io/images/blog/2022/vscode/vsc4.jpg)

可以直接打开编辑 `.xmind` 的文件，不过快捷键设置上我更喜欢上面那个。

4） draw.io

![](https://skywind3000.github.io/images/blog/2022/vscode/vsc5.jpg)

很多人推荐过的矢量图工具，我是重度使用的，如果说上面两个记笔记和脑图的插件我也还是同时会用其他笔记和脑图的软件，那么矢量图方面，我只用 draw.io，功能强，专业度高。

5）Dictionary Completion

![](https://skywind3000.github.io/images/blog/2022/vscode/vsc6.jpg)

字典补全，可以设置一个常用英文单词词典，然后辅助你输入单词的，写英文文档很有帮助，有些长单词知道怎么读，但是写出来经常写错的，有这个就好办了，支持模糊匹配，拿不准时随意输入点你记得的部分，它也能给你推荐最接近的。

6）HexEditor

![](https://skywind3000.github.io/images/blog/2022/vscode/vsc7.jpg)

二进制编辑器，安装后在左边文件树那里选择一个文件，鼠标右键 “Open With" 然后选择 HexEditor 打开即可，偶尔需要编辑下二进制时，不需要再去下载安装一个专门软件。

7）Bookmarks

![](https://skywind3000.github.io/images/blog/2022/vscode/vsc8.jpg)

经常在文档几个不同位置跳来跳去的，这个书签插件很实用，右键菜单里直接设置/取消书签，快捷键在不同的书签位置跳转，左边还有当前书签列表，双击立马跳转。

8）GitHub Repositories

![](https://skywind3000.github.io/images/blog/2022/vscode/vsc9.jpg)

打开远程 github 仓库，F1 选择 Remote Repositories: Open Remote Repository 然后帖任意一个 github 项目的 url 就能打开了：

![](https://skywind3000.github.io/images/blog/2022/vscode/vsc10.jpg)

有时候网页上读某个 github 项目的代码太麻烦，全部 clone 下来太费时间，用这个插件就可以快速打开远程仓库，按需请求文件内容，读起代码来飞快。

9）MetaJump

![](https://skywind3000.github.io/images/blog/2022/vscode/vsc11.jpg)

快速光标移动，类似 vim 里的 easymotion，如果你经常使用键盘，那么按 ALT+/ 然后再随便敲一个字母，比如上图中敲了个小写字母 "n" ，然后屏幕内所有出现 "n" 的地方都被蓝色高亮起来，并且上面覆盖了一个快捷字母，再按一下相应字母，就可以直接跳到该处，比如再按一下 "a" 就能跳到 13 行的 "notebook...." 的 "n" 字母上。

总共按三次键就可以移动到屏幕内任意地方，用熟了基本指哪打哪。

10）Blockman

![](https://skywind3000.github.io/images/blog/2022/vscode/vsc12.jpg)

很酷的一款小插件，用浅显的背景色，直观的展示代码的层次结构。

11）Window Colors

![](https://skywind3000.github.io/images/blog/2022/vscode/vsc13.png)

适合多开 vscode 的同学们，看着几个 vscode 窗口经常蒙圈找不到谁是谁的，可以为每个项目制定一个专属的颜色，多开窗口再也不会迷路。

12）todo tree

![](https://skywind3000.github.io/images/blog/2022/vscode/vsc14.png)

找出代码里所有包含：`TODO` 和 `FIXME` 的注释，并且列在左边面板中，方便你快速定位代码里的 `TODO`。 有时候代码不会一次写完，有时候某处只是先用一个临时方案，后面还需要继续完善，这时候人们习惯在注释里加一条 `TODO` 字样，这个插件就是帮你快速列出项目内所有文件还需要完成的任务，避免遗漏某些需要进一步完善的地方。

--

12个凑够一打了，先写这些吧。

