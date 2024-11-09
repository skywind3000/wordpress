---
uuid: 3171
title: Vim2022：实时代码格式化
status: publish
categories: 未分类
tags: Vim
slug: 
date: 2021-12-14 01:11
---
大部分 IDE/编辑器 都有代码格式化的功能或者插件，但都需要你主动触发格式化命令，而且每次写很多代码在保存的时候一次性格式化，总会有种不放心的感觉，需要跳过头去检查。

有没有可能让我一边写一边实时格式化呢？这样每次我都能看到最终的效果。

于是我写了个小脚本 [vim-rt-format](https://github.com/skywind3000/vim-rt-format)，再 INSERT 下面每次按回车就能自动格式化当前行：

![](https://skywind3000.github.io/images/p/pep/rtformat_4.gif)

有了这个东西以后，写代码爽多了，释放注意力，完全专注于 “编码”，再也不用为 “格式化”这个事情花费额外的精力，变量名和运算符之间无需加空格，直接回车就自动变成干净清爽的代码了，能自动识别语法元素，并且格式化的过程无需离开 INSERT 模式。

目前支持：Python, Lua, Javascript 几种语言，使用的话，只需要 Vim 支持 +python3 特性，且 Python 安装 autopep8 模块即可，配置如下：

```vim
" 使用 vim-plug 安装插件
Plug 'skywind3000/vim-rt-format'

" 默认在 INSERT 模式下按 ENTER 格式化当前代码行，将下面设置
" 成 1 的话，可以用 CTRL+ENTER 来格式化，ENTER 将保留原来的功能
let g:rtf_ctrl_enter = 0

" 离开 INSERT 模式的时候再格式化一次
let g:rtf_on_insert_leave = 1
```

行了，保存配置并重启 Vim，随便打开一个源代码开始编辑，就是这么简单。

你会忽然发现，天空变得更加晴朗，空气变得更加的清新，多么美好的一天啊。

项目主页：

[https://github.com/skywind3000/vim-rt-format](https://github.com/skywind3000/vim-rt-format)


