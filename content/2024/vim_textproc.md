---
uuid: 2998
title: Vim 文本过滤/文字处理插件
status: publish
categories: 随笔
tags: Vim
slug: 
date: 2024-10-13 23:30
---
我经常有文本处理的需求，例如将 html 转换成纯文本，或者移除 markdown 里的所有连接，或者繁体转换简体。因此我做了一个插件来管理和执行各种外部文本过滤器。

所谓 “文本过滤器” 是一个命令行程序，它从标准输入读取文本，然后进行一些处理后写到标准输出，在 Vim 里可以用原生的 `:{range}! xxx` 命令将选中文本发送给 xxx 命令的标准输入，然后用该命令的标准输出替换选中文本，这个命令很有用，但每次输入一长串命令略显繁琐，并且过滤器多了以后也很难管理。

因此我做了这个插件来统一管理文本过滤程序，并且提供接口来执行他们：

![](https://skywind3000.github.io/images/p/textproc/tp1.gif)

比如上图演示了将 HTML 转换成文本，以及去除 markdown 中的连接，使用命令 `:{range}TP {name}` 就能调用名为 `{name}` 的文本过滤程序了。这些程序可以用你喜欢的语言编写，放到统一的目录，加上可执行属性就行，该插件就能找到它。

<!--more-->

而你在调试你的文本过滤脚本时，可以加个叹号 `:{range}TP! {name}` 这样你就可以在另一个窗口里预览结果，而不会覆盖到原文本：

![](https://skywind3000.github.io/images/p/textproc/tp2.gif)

这样调试起来比较方便反复运行。

编写一个文本过滤脚本也很简单，比如在 `~/.vim/text` 目录内创建 "markdown_to_dokuwiki.sh" 文件：

```bash
#! /usr/bin/bash
pandoc -f markdown-simple_tables-multiline_tables+pipe_tables -t dokuwiki
```

就可以用 `:%TP markdown_to_dokuwiki` 命令将当前窗口内的 markdown 转换成 dokuwiki 语法。

插件地址：

https://github.com/skywind3000/vim-text-process

今天我数了一下，不知不觉我已经开发了 20 个 Vim 插件了：

https://skywind.me/wiki/vim_plugins

欢迎尝试。

