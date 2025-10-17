---
uuid: 1708
title: GVim 中更好的运行程序
status: publish
categories: 随笔
tags: Vim
date: 2016-05-09 16:24:10
---
GVim（Windows）下面使用!运行程序是非常恶心的事情，比如调用python运行当前脚本：

```vim
:!python %
```

你会发现，整个VIM界面被冻结了，然后弹出cmd窗口，退出cmd后，还要返回GVim中按任意键才能编辑状态。

比如你正在调试一个程序，这个程序运行起来不是一分钟能出结果的时候，你想边对照输出结果，边在 GVim 里面查看和修改你的代码，你就会发现傻逼了。正确的做法是：

```vim
:!start python %
```

这样就不会卡住 Vim了，但是这个做法有个问题，程序结束的时候窗口马上关闭，因此还需要再进化一下：

```vim
:silent !start cmd /c python % & pause
```

这时你会发现优雅的调用了 python 来跑当前程序，并且GVIM不会被挂起，照样可以编辑，当程序结束的时候，CMD窗口还会pause等待你按任意键一下，这就比较清爽了，你可以把这条命令map到你常用的快捷键上，和 EditPlus里面一样一键运行之。

然而还是有几处需要完善的地方，首先直接使用 `%` 展开当前文件名不妥当，如果文件名包含空格就会错误，需要用 `shellescape` 来进行处理，同时我们有时候还希望运行前跳转到文件所在的目录，运行完又跳转回来，又或者需要运行前保存一下没有保存的文件。

我写了个函数来做这个事情，放到你 .vimrc里即可使用，同时支持 GVim和终端 Vim：

<!--more-->

```vim
" run current file by detecting file extname. if cwd is non-zero, 
" it will change the current directory to the file location.
" Unsaved files will be saved if needsave is non-zero
function! VimExecute(cwd, needsave)
	let savecwd = getcwd()
	let cd = haslocaldir()? 'lcd ' : 'cd '
	let ext = tolower(expand("%:e"))
	if bufname('%') == '' 
		return 
	endif
	if a:needsave != 0
		silent! update 
	endif
	if a:cwd != 0
		let dest = expand('%:p:h')
		silent! exec cd . fnameescape(dest)
	endif
	if has('gui_running') && (has('win32') || has('win64') || has('win95'))
		let fname = shellescape(expand("%"))
		if index(['c', 'cpp'], &filetype) >= 0
			exec '!start cmd /C '. shellescape(expand("%<")) . ' & pause'
		elseif index(['py', 'pyw', 'pyc', 'pyo'], ext) >= 0
			silent exec '!start cmd /C python ' . fname . ' & pause'
		elseif ext  == "js"
			silent exec '!start cmd /C node ' . fname . ' & pause'
		elseif ext == 'sh'
			silent exec '!start cmd /C sh ' . fname . ' & pause'
		elseif ext == 'lua'
			silent exec '!start cmd /C lua ' . fname . ' & pause'
		elseif ext == 'pl'
			silent exec '!start cmd /C perl ' . fname . ' & pause'
		elseif ext == 'rb'
			silent exec '!start cmd /C ruby ' . fname . ' & pause'
		elseif ext == 'php'
			silent exec '!start cmd /C php ' . fname . ' & pause'
		elseif ext == 'ps1'
			silent exec '!start cmd /C powershell '. fname. ' & pause'
		endif
	else
		if index(['c', 'cpp'], &filetype) >= 0
			exec '!'. shellescape(expand("%<"))
		elseif index(['py', 'pyw', 'pyc', 'pyo'], ext) >= 0
			exec '!python ' . shellescape(expand("%"))
		elseif ext  == "js"
			exec '!node ' . shellescape(expand("%"))
		elseif ext == 'sh'
			exec '!sh ' . shellescape(expand("%"))
		elseif ext == 'lua'
			exec '!lua ' . shellescape(expand("%"))
		elseif ext == 'pl'
			exec '!perl ' . shellescape(expand("%"))
		elseif ext == 'rb'
			exec '!ruby ' . shellescape(expand("%"))
		elseif ext == 'php'
			exec '!php ' . shellescape(expand("%"))
		elseif index(['osa', 'scpt', 'applescript'], ext) >= 0
			exec '!osascript '. shellescape(expand('%'))
		elseif ext == 'ps1'
			exec 'powershell '. shellescape(expand('%'))
		endif
	endif
	if a:cwd != 0
		silent! exec cd . fnameescape(savecwd)
	endif
endfunc


```

这个函数有两个参数，第一个参数非零的话，会在运行前跳转到文件所在目录，运行后又跳回来。第二个参数非零的话，能自动保存未保存的文件，同时支持 GVim和终端 Vim.

你可以把该函数绑定到 F5上，自动判断是否运行在GVIM下面，并用正确的方式执行当前代码，函数中几处外部调用用来判断文件是否需要保存，以及是否需要切换到文件当前目录的地方，你可以按需要扩充。

![](https://skywind3000.github.io/images/t/misc/donation.png)


