---
uuid: 3174
title: Vim2021：超轻量级代码补全系统
status: publish
categories: 未分类
tags: Vim
slug: 
date: 2021-02-04 14:04
---
2121年了，应该尝试些新东西，这里介绍一个超级轻量级（169 行代码）的代码补全系统，针对：历史输入，字典，tags 等多个源提供类似 YouCompleteMe 的操作体验，并且无需安装各种后端的补全 LSP 服务器。

语义补全是很爽，但有时候，当你用某些缺乏 LSP 支持的小众语言写代码时，或者你去到一台临时的服务器上工作时，你并不想花时间编译和设置一套复杂的补全系统。

这种时候，其实 Vim 内建补全系统其实就已经足够你用了，它能从当前文件收集单词，能从 dict 文件以及 tags 文件收集单词，并且在你按下 `<c-n>` 或者 `<c-x><c-k>` 时弹出补全框。

这个小脚本就是在你每次输入 1-2 个字符的时候为你自动弹出补全窗口用的，并且提供类似 YouComplete 的补全体验（点击查看 GIF 动图）：

![](https://skywind3000.github.io/images/p/auto-popmenu/demo.gif)

#### 特性说明：

- 自动弹出补全框。
- 使用 TAB 和 SHIFT+TAB 来循环选择补全内容，`<c-e>` 关闭补全框。
- 提供同 YouCompleteMe 完全一致的体验（针对：buffer, dict, tags 几个源）。
- 纯绿色，所有操作都是对当前 buffer 生效，不会影响其他 buffer。
- 能够和其他补全系统一起共存（可以设置只对某些文件或者 buffer 生效）。
- 无需种量级补全服务，无需编译后台 LSP 模块。
- 轻量级，响应快，比大部分补全系统反应都要灵敏。
- 只有一个 160 行的 apc.vim 文件，你甚至可以直接把内容拷出来粘贴到你 vimrc 里。
- 适合作为各种大型补全系统的一个理想备份方案。

#### 如何使用？

只需要这样就行了：（点击 more/continue 继续）

<!--more-->

```vim
Plug 'skywind3000/vim-auto-popmenu'

" 设定需要生效的文件类型，如果是 "*" 的话，代表所有类型
let g:apc_enable_ft = {'text':1, 'markdown':1, 'php':1}

" 设定从字典文件以及当前打开的文件里收集补全单词，详情看 ':help cpt'
set cpt=.,k,w,b

" 不要自动选中第一个选项。
set completeopt=menu,menuone,noselect

" 禁止在下方显示一些啰嗦的提示
set shortmess+=c
```

也许你还会需要一个字典插件，为众多语言提供字典数据，还有一份英文单词字典，能在你编写文本文件和 markdown 的时候提供英文单词补全（类似上面的 GIF 截图里的效果）：

```vim
Plug 'skywind3000/vim-dict'
```

这就是你所需要的全部了。

#### 常用命令

- `ApcEnable`：为当前文档开启补全（比如你没有设置上面的 `g:apc_enable_ft` 时）。
- `ApcDisable`：为当前文档禁用补全
只有上面两条命令，并且只对当前文档生效，不会影响其他文件。

#### 插件共存

以 YouCompleteMe 为例，共存的话，先要设置 YCM 禁用某些文档：

```vim
let g:ycm_filetype_blacklist = {'text':1, 'markdown':1, 'php':1}
```

这样编辑上面三种文件时 YCM 就不生效了，因为它本来也不支持这三种文件的语义补全，接着我们设置对这三种文件自动运行这个补全小脚本：

```vim
let g:apc_enable_ft = {'text':1, 'markdown':1, 'php':1}
```

这样这三种文件我们就用这个 apc.vim 的小脚本进行补全了，由于这三种类型的代码，YCM 本身语义补全的优势又发挥不出来，而这个小脚本还能比 YCM 多提供一个字典补全，因此这些没有语义补全支持的文件类型上，这个小脚本的体验是可以比其他补全系统好的。

再，由于就一个 160 行的 apc.vim 脚本，很容易随着你的 vimrc 一起部署，用的时候只要扔到 ~/.vim/plugins 目录下面就能自动运行了，或者在 vimrc 最后：

```vim
source /path/to/apc.vim
```

粗暴点，把 apc.vim 内容拷贝出来，直接粘贴在你 vimrc 里面也行，本身也没几行。

再 LSP 无法工作或者不想费力安装 LSP 的情况下，它为你提供一个基本能用的补全系统。

#### 地址：

[https://github.com/skywind3000/vim-auto-popmenu/](https://github.com/skywind3000/vim-auto-popmenu/)

