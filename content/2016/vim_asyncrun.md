"=========== Meta ============
"StrID : 1835
"Title : Vim 异步运行 Shell 指令的插件 - AsyncRun
"Slug  : 
"Cats  : 随笔
"Tags  : Vim
"=============================
"EditType   : post
"EditFormat : Markdown
"TextAttach : 
"========== Content ==========
自制另一个新的 Vim 8.0 专用异步插件：[asyncrun.vim](https://github.com/skywind3000/asyncrun.vim)，它可以让你在 Vim 里面异步运行各种 Shell 指令并且把结果实时输出到 Quickfix，需要 Vim 7.4.1829 以上版本。

**安装方法**

到插件首页 [https://github.com/skywind3000/asyncrun.vim](https://github.com/skywind3000/asyncrun.vim) 下载项目，并拷贝 `asyncrun.vim` 到你的 `~/.vim/plugin`。或者使用 Vundle 指向 `skywind3000/asyncrun.vim` 来自动更新。


**基本教程**

使用 gcc 异步编译当前文件：

```text
:AsyncRun gcc % -o %<
:AsyncRun g++ -O3 % -o %< -lpthread 
```

该命令会在后台运行 gcc 并且把输出实时显示在 Quickfix 窗口，宏 `%` 代表当前文件名，`%<` 代表没有扩展名的文件名。

异步运行 make：

```text
:AsyncRun make
:AsyncRun make -f makefile
```


异步调用 grep:

```text
:AsyncRun! grep -R word . 
:AsyncRun! grep -R <cword> .
```

默认 :AsyncRun 运行命令后，输出添加到 Quickfix时 Quickfix 会自动滚动到最下面那一行，使用感叹号修饰符以后，可以避免 Quickfix 自动滚动。同时 `<cword>` 代表当前光标下面的单词。
 

编译 go项目：

```text
:AsyncRun go build %:p:h
```

宏 `%:p:h` 代表当前文件的目录

查询 man page，异步 git push ，以及把设置 F7异步编译当前文件：

```text
:AsyncRun! man -S 3:2:1 <cword> 
:AsyncRun git push origin master
:noremap <F7> :AsyncRun gcc % -o %< <cr> 
```

**使用手册**

AsyncRun - Run shell command：

```text
:AsyncRun{!} [cmd] ...
```

后台运行命令并且实时输出到 quickfix 窗口，如果有感叹号修饰符，quickfix 窗口的自动滚动将会禁止。

命令参数以空格分割，接受下面这些以 '`%`', '`#`' or '`<`' 开头的替换宏:

```text
%:p     - File name of current buffer with full path
%:t     - File name of current buffer without path
%:p:h   - File path of current buffer without file name
%:e     - File extension of current buffer
%:t:r   - File name of current buffer without path and extension
%       - File name relativize to current directory
%:h:.   - File path relativize to current directory
<cwd>   - Current working directory
<cword> - Current word under cursor
<cfile> - Current file name under cursor
```

运行一个命令前，环境变量也会做如下设置:

```text
$VIM_FILEPATH  - File name of current buffer with full path
$VIM_FILENAME  - File name of current buffer without path
$VIM_FILEDIR   - Full path of current buffer without the file name
$VIM_FILEEXT   - File extension of current buffer
$VIM_FILENOEXT - File name of current buffer without path and extension
$VIM_CWD       - Current directory
$VIM_RELDIR    - File path relativize to current directory
$VIM_RELNAME   - File name relativize to current directory 
$VIM_CWORD     - Current word under cursor
$VIM_CFILE     - Current filename under cursor
$VIM_GUI       - Is running under gui ?
$VIM_VERSION   - Value of v:version
$VIM_MODE      - Execute via 0:!, 1:makeprg, 2:system()
$VIM_COLUMNS   - How many columns in vim's screen
$VIM_LINES     - How many lines in vim's screen
```

AsyncStop - Stop the running job:

```text
:AsyncStop{!}
```

停止后台任务（使用 TERM信号），如果有感叹号修饰，则使用 KILL 信号结束

基本设置:

```text
g:asyncrun_exit - 字符串，如果不为空那么任务结束时会被执行（VimScript）
g:asyncrun_bell - 如果非零的话，任务结束后会响铃（终端输出控制符 \a）
g:asyncrun_mode - 0:异步(需要 vim 7.4.1829) 1:同步 2:直接运行
```

全局变量:

```text
g:asyncrun_code   - 退出码
g:asyncrun_status - 状态 'running', 'success' or 'failure'
```


如果你喜欢的话请为我投一票：
[http://www.vim.org/scripts/script.php?script_id=5431](http://www.vim.org/scripts/script.php?script_id=5431)



