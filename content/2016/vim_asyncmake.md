---
uuid: 1813
title: Vim 异步编译插件 vimmake
status: publish
categories: 随笔
tags: vim
---
推荐下自己写的用了好几年的编程插件：vimmake ？完美支持 vim的异步模式：
[GitHub - skywind3000/vimmake: Customize shell commands in vim](https://github.com/skywind3000/vimmake)

让用户自定义各种不同的编译或运行任务，并且在 Vim 中执行他们。类似 NotePad++的自定义 Commands 和 EditPlus/UltraEdit 的 'User Tool' 或者 GEdit中的 External Tool 以及 TextMate 中的 Shell Command。完美支持 vim 7.4.1829 后已经稳定成熟的异步任务机制，不需要写任何 Vim Script 也可以很容易的体验到 vim 的异步任务机制，并且使用它来执行各种艰巨的编译任务，让你一边编辑代码，一边跑编译任务。

安装：拷贝 vimmake.vim 到你的 ~/.vim/plugin 或用 vundle 指向 skywind3000/vimmake .


**简单使用：异步编译 & 运行 C/C++ 代码**

首先每个 “用户自定义工具” 使用一个独立的 shell脚本来描述（Windows下是.cmd的批处理文件），我们将首先编写 vimmake可以使用的 gcc编译工具脚本， "~/.vim/vimmake.gcc":

```bash
#! /bin/sh
gcc "$VIM_FILEPATH" -o "$VIM_FILEDIR/$VIM_FILENOEXT"
```

就这么短短的两行，当你把它设置成 0755的权限时，就可以在 Vim中通过下面语句运行了：

```vim
:VimTool gcc
```

命令 `:VimTool {name} ` 命令会在 Vim里面直接调用 ~/.vim/ 目录下，名为 "vimmake.{name}" 的脚本来完成各种类似编译或者执行的任务，所以用`:VimTool gcc` 就可以运行前面定义的名为 vimmake.gcc 的工具脚本来编译当前的源代码了。

现在编辑 "~/.vim/" 下面名为 "vimmake.run" 的脚本，以便用 `:VimTool run` 来运行当前代码：

```bash
#! /bin/sh
"$VIM_FILEDIR/$VIM_FILENOEXT"
```

记得将 vimmake.run 的模式设置成 0755，如今有了两个可以直接在 Vim里通过 VimTool命令启动的工具（gcc 和 run），接下来我们需要设置 run 这个工具的模式为默认运行模式，而 gcc 为 quickfix模式（输出会被捕获并重定向到 quickfix窗口），现在打开 .vimrc 添加一行：

```vim
let g:vimmake_mode = { 'gcc':'quickfix', 'run':'normal' }
```

而如果我们能够使用到较新版本的 vim（7.4.1829或者更高），我们就可以使用异步方式在后台启动 gcc，并且将后台进程的输出实时重定向到界面下端的 quickfix 窗口：

```vim
let g:vimmake_mode = { 'gcc':'async', 'run':'normal' }
```

在这之后，将 'gcc'的运行模式设置成 'async' 后，`:VimTool gcc` 就可以以异步的方式运行名为 vimmake.gcc 的脚本然后在后台执行编译任务了，就像传统 IDE编译任务一样。

以往使用 Vim 的 :make 之类的命令编译项目时，往往无法异步，编译任务一运行，你就无法编辑了，只有等到编译结束，才能返回编辑状态，大项目时，不得不另外开一个终端来进行编译，这是很痛苦的事情，有了异步任务以后，你能在同一个屏幕下编辑并且实时在 quickfix窗口查看编译的进度。

vimmake 可以让你在不需要掌握晦涩的 VimScript 和繁琐的异步编程接口的情况下，直接方便的使用vim 异步功能来完成各种长时间编译任务。同时为了加快你的：编译-编辑-编译 工作流的流畅度，我们需要配置一两个热键来调用 `:VimTool` 命令：

```vim
noremap <F7> :VimTool gcc<cr>
noremap <F5> :VimTool run<cr>
inoremap <F7> <ESC>:VimTool gcc<cr>
inoremap <F5> <ESC>:VimTool run<cr>
```

在 .vimrc里面加入上面的几行代码，你就可以方便的按 F7编译当前文件，F5运行之了。和GEdit
类似，VimTool命令在运行具体工具脚本前会设置若干环境变量来记录当前编辑的文件名，路径，当前vim工作目录等一系列信息，然后在工具脚本里面可以直接取出这些值来调用需要的外部工具链：
如上图，后台运行工具脚本进行编译，并且编译器的输出会被实时显示到下面的 quickfix窗口，选中错误的那行输出，会直接跳转：

![](https://raw.githubusercontent.com/skywind3000/vimmake/master/images/screen1.gif)

<!--more-->

**命令解释：VimTool - 执行用户自定义工具**

下面这条命令会运行名为 "~/.vim/vimmake.{name}" 的脚本：

```
:VimTool {name}
```

在 Windows下的话，会运行名为： "C:\Users\yourname\.vim\vimmake.{name}.cmd" 的批处理。

{name} 后面还可以跟随一个名为 {target} 的参数：

```
:VimTool {name} {target}
```

`{target}` 的内容会作为环境变量：$VIM_TARGET 传入到 `vimmake.{name}` 的脚本中。工具脚本可以使用这个值作为 make target 当作第一个参数传给 make程序。`:VimTool` 命令在调用每个工具脚本前，会初始化下面一些系统环境变量供脚本使用：

| Environment Variable | Description |
|----------------------|-------------|
| $VIM_FILEPATH | File name of current buffer with full path |
| $VIM_FILENAME | File name of current buffer without path |
| $VIM_FILEDIR | Full path of current buffer without the file name |
| $VIM_FILEEXT | File extension of current buffer |
| $VIM_FILENOEXT | File name of current buffer without path and extension |
| $VIM_CWD | Current directory |
| $VIM_RELDIR | File path relativize to current directory |
| $VIM_RELNAME | File name relativize to current directory  |
| $VIM_CWORD | Current word under cursor in the buffer |
| $VIM_GUI | Is it running in gui ? |
| $VIM_VERSION | Value of v:version |
| $VIM_MODE | Execute via 0:bang(!), 1:makeprg, 2:system(), ... |
| $VIM_SCRIPT | Home path of tool scripts |
| $VIM_TARGET | Target given after name as ":VimTool {name} {target}" |
| $VIM_COLUMNS | How many columns in vim's screen |
| $VIM_LINES | How many lines in vim's screen |

在工具脚本中使用上面这些环境变量，你可以自由的编译当前的 Makefile，或者编译和运行单个文件，或者编译你的 latex，或者在当前目录下异步执行一下grep，或者把当前光标下的单词传递给外部的 man 帮助 、命令行字典程序并把结果取回来显示到 quickfix窗口中。或者对当前编辑文件简单运行一下 svn diff指令并同样也把结果显示到quickfix里。

**命令解释：VimStop**

停止当前后台任务（如果使用async模式运行的话），VimStop! 可以发送-9号信号强制杀死后台进程，一般很少用。

**参数配置：**

g:vimmake_mode (dictionary) - 运行模式

g:vimmake_mode 是一个字典，你可以在 .vimrc中这样初始化不同工具的运行模式：

```vim
let g:vimmake_mode = {}
let g:vimmake_mode['gcc'] = 'async'
let g:vimmake_mode['run'] = 'normal'
```

运行模式可以有下面几种:

```
normal   默认模式，运行工具并等待结束后返回vim（win下弹出窗口运行，不必等待）
quickfix 运行工具并等待结束后返回vim，把结果输出到 quickfix
bg       在后台运行工具，并且忽略任何输出。
async    异步任务方式在后台运行工具，并且把输出实时显示在 quickfix中
```

上面四种运行模式，只有 async模式需要 vim 7.4.1829 以上支持，其他三种 7.0以后都支持，如果不设置的话，将会启用默认的 normal模式。如果你需要打开一个新的窗口的模式运行一个脚本，那么你在工具脚本中需要自己调用 gnome-terminal 或者 xterm之类的工具来完成，如果在 Mac下面的话，可以用 open 命令来打开新终端窗口并运行你的程序。

模式 quickfix 和 async 都会把脚本的输出导向 quickfix窗口，如果你不知道怎么在 vim下面打开quickfix窗口的话，可以用 `:copen 8` 命令 或者 `:botright copen 8` 命令在不同位置打开 quickfix窗口，具体quickfix的操作细节见：`:help quickfix`。

g:vimmake_path (string) - 设置工具脚本路径

默认工具脚本都是保存在 ~/.vim/ 目录下面，你可以通过修改这个变量更改成其他位置：

```vim
let g:vimmake_path = '/home/myname/github/config/tools'
``` 

这样 `:VimTool {name}` 就会在新的路径下 运行 vimmake.{name} 这个脚本了，如此，你可以方便的把你的一系列工具脚本放到你的 github 仓库中，并且在不同的地方愉快的同步了。

g:vimmake_save (int) - 是否保存当前文件 ?
如果设置成1，那么 VimTool 运行工具脚本前会保存当前正在编辑的文件。

g:vimmake_build_scroll (int) - 是否自动滚动 quickfix 窗口 ?
在使用async模式运行编译任务时，如果这个值被设置成1，那么随着编译器的输出被不断的显示到 quickfix窗口，quickfix会自动滚动到最下面那行，保证你能实时查看最新的输出。

g:vimmake_build_post (string) - 异步任务结束后会触发什么命令？
当异步任务执行完后, g:vimmake_build_post 中保存的 VimScript 会被自动执行，可以被用来调用外部工具，比如在编译结束后调用 afplay来播放一个wav文件:

```vim
let g:vimmake_build_post = "silent call system('afplay ~/.vim/notify.wav &')"
```

这样当你眼镜盯着代码看的时候就不必当心编译结束了你还不知道，afplay是 mac os x 下命令行播放 wav文件的程序，Windows下你可以使用：

https://github.com/skywind3000/support/blob/master/tools/playwav.exe

这个工具来播放音效：

	let g:vimmake_build_post = 'silent !start playwav.exe "C:/Windows/Media/Windows Error.wav" 200'

Gvim中 !start 可以无需等待的运行外部命令，通过播放悦耳的音效，可以让你的：编译-编辑-编译 工作流更加高效，在你潜意识里让你心情愉悦，哪怕你为了找恶心的 bug而抓狂时，选择一个动听的音效能鼓励你不断的继续下去。

使用案例：更好的运行当前文件

在 ~/.vim 路径下创建新版本的 vimmake.run 文件，并编辑：

```bash
#! /bin/sh

cd "$VIM_FILEDIR"

case "$VIM_FILEEXT" in 
    \.c|\.cpp|\.cc|\.cxx)
        "$VIM_FILEDIR/$VIM_FILENOEXT"
        ;;
    \.py|\.pyw)
        python "$VIM_FILENAME"
        ;;
    \.pl)
        perl "$VIM_FILENAME"
        ;;
    \.lua)
        lua "$VIM_FILENAME"
        ;;
    \.js)
        node "$VIM_FILENAME"
        ;;
    \.php)
        php "$VIM_FILENAME"
        ;;
    *)
        echo "unexpected file type: $VIM_FILEEXT"
        ;;
esac
```

这是上面那个简单的 vimmake.run 的高级版本，它能够根据环境变量 $VIM_FILEEXT自动判断文件的类型，并且调用不同的方法来运行当前文件。

工具脚本可以用 bash来写，也可以用其他你喜欢的 perl 或者 python 来完成，只需要修改下第一行的：“#! " 指定一个新的解释器即可，记得将 vimmake.run 这个文件设置成 0755的模式，以便有权限运行它，然后把 `:VimTool run` 命令隐射到 F5上面，每次你按 F5就触发这个脚本，智能的运行你的文件。

使用案例：异步方式跑 Makefile

十分简单，把下面的脚本保存成：~/.vim/vimmake.make 然后用 `:VimTool make` 触发即可：

```bash
#! /bin/sh
make $VIM_TARGET
```

记得把运行模式配制成 async （低版本 vim的话配制成 quickfix）。

使用案例：在 man手册中查询当前的字符

把下面脚本保存成 ~/.vim/vimmake.man ，然后用 `:VimTool man` 来触发（最好绑定热键）。

```bash
#! /bin/sh
WIDTH=`expr $VIM_COLUMNS - 10`
man -S 3:2:1 -P cat "$VIM_CWORD" | fold -w $WIDTH
```

这个也不难，同样设置成 async模式，按下热键，就会用man查询当前光标下的命令，并且在quickfix中显示出来，是不是很爽？你还可以配置一个命令行字典（有很多命令行字典程序）， 服务器上用 Vim 查看文档时一个快捷键，就显示出当前单词的翻译了。

**使用案例：编译 golang 源代码**

我们经常会碰到新的语言和新的工具链，这时以其苦苦等待该语言的vim插件，不如直接用vimmake自己动手设置下，即可编译 go代码，编辑脚本：~/.vim/vimmake.go：

```bash
#! /bin/sh
go build "$VIM_FILEPATH"
```

同样很简单，使用 `:VimTool go` 来编译当前go代码，并将输出导向 quickfix，一个新的工具链就这么简单几下设置好了，最后别忘记记再仿照前面设置一下我们的热键：

```vim
noremap <F7> :VimTool gcc<cr>
noremap <F5> :VimTool run<cr>
noremap <F8> :VimTool go<cr>
inoremap <F7> <ESC>:VimTool gcc<cr>
inoremap <F5> <ESC>:VimTool run<cr>
inoremap <F8> <ESC>:VimTool go<cr>
```

**使用案例：热键打开/关闭 quickfix 窗口**

由于大量使用 quickfix 来查看工具输出，我们需要直接用<F10> 来切换显示：

```vim
noremap <F10> :silent call vimmake#Toggle_Quickfix()<cr>
inoremap <F10> <ESC>:silent call vimmake#Toggle_Quickfix()<cr>
```

因为高频使用，所以我在 vimmake 里面提供了这个切换函数，直接配置到你喜欢的热键上，使用即可。

**使用案例：Windows下更好的执行文件**

如果在 Windows下，我们可以用编写 “vimmake.run.cmd” 这个批处理来完成：

```bat
@ECHO OFF
if "%VIM_FILENAME%" == "" GOTO ERROR_NO_FILE
CD /D "%VIM_FILEDIR%"

if "%VIM_FILEEXT%" == ".c" GOTO RUN_MAIN
if "%VIM_FILEEXT%" == ".cpp" GOTO RUN_MAIN
if "%VIM_FILEEXT%" == ".cc" GOTO RUN_MAIN
if "%VIM_FILEEXT%" == ".cxx" GOTO RUN_MAIN
if "%VIM_FILEEXT%" == ".py" GOTO RUN_PY
if "%VIM_FILEEXT%" == ".pyw" GOTO RUN_PY
if "%VIM_FILEEXT%" == ".bat" GOTO RUN_CMD
if "%VIM_FILEEXT%" == ".cmd" GOTO RUN_CMD
if "%VIM_FILEEXT%" == ".js" GOTO RUN_NODE

echo unsupported file type %VIM_FILEEXT%
GOTO END

:RUN_MAIN
"%VIM_FILENOEXT%"
GOTO END

:RUN_PY
python "%VIM_FILENAME%"
GOTO END

:RUN_CMD
cmd /C "%VIM_FILENAME%"
GOTO END

:RUN_NODE
node.exe "%VIM_FILENAME%"
GOTO END

:ERROR_NO_FILE
echo missing filename
GOTO END

:END
```

批处理的位置需要放置在：C:\Users\用户名\.vim 下面（当然你可以通过 g:vimmake_path 配置修改这个位置）。

使用案例：Windows 下调用 mingw 来编译

在 "C:\Users\YourName\.vim" 下面新建批处理文件 vimmake.gcc.cmd：

```bat
@ECHO OFF
if "%VIM_FILENAME%" == "" GOTO ERROR_NO_FILE

d:\dev\mingw32\bin\gcc -Wall -O3 -std=c++11 "%VIM_FILEPATH%" -o "%VIM_FILEDIR%/%VIM_FILENOEXT%" -lwinmm -lstdc++ -lgdi32 -lws2_32 -msse3 -static
GOTO END

:ERROR_NO_FILE
echo missing file name

:END
```

这样即可，记得把 g:vimmake_mode['gcc'] 的值设置成 async 或者 quickfix，这样编译错误才能保证输出到 quickfix 窗口。

前面说了很多 unix下的用法，所以补充几段 Windows 的，记得 gvim 用官方的 daily build：
[Releases · vim/vim-win32-installer · GitHub](https://github.com/vim/vim-win32-installer/releases)

**使用案例：在状态栏显示编译状态**

异步任务有三种状态: running, success 和 failure。可以编辑 .vimrc 在 quickfix的 statusline上面显示编译的状态：

```vim
augroup QuickfixStatus
    au! BufWinEnter quickfix setlocal 
        \ statusline=%t\ [%{g:vimmake_build_status}]\ %{exists('w:quickfix_title')?\ '\ '.w:quickfix_title\ :\ ''}\ %=%-15(%l,%c%V%)\ %P
augroup END
```

全局变量 g:vimmake_build_status 用来实时表示异步任务状态:

```
running: 异步任务开始时被设置
success: 异步任务成功时被设置（工具脚本返回 0的进程结束码）
failure: 异步任务失败时被设置（工具脚本返回非 0的进程结束码）
```

这样你就可以在 quickfix 窗口的 statusline上实时查看编译进度了，返回值不用特异处理，调用完 gcc后正常结束你的工具脚本即可，bash 或者批处理会自动继承上一次外部进程的返回值作为自己进程结束的返回值，gcc在成功后会自动返回0，失败自动返回非零，这样会正确的影响到我们的 g:vimmake_build_status 变量。

**使用案例：在新窗口中运行程序**

如果你在非终端下开发一些长时间运行的程序（比如一个简单的 HttpServer demo），往往你需要再开一个终端来运行它，这样的你可以一边编写代码，一边查看运行状态，但是现在我们有更好的方式：直接从vim里面打开一个新的终端窗口来运行它。

当你在 windows 的 gvim里面下使用 vimmake 来运行工具的话，默认的 normal模式每次都会打开一个新窗口来运行（使用 gvim里面的 `:!start`命令，而不是 windows 下面弱智的 `:!`命令）：

![](http://skywind3000.github.io/word/images/screen2.gif)

但如果你跑在 ubuntu 下，就需要写几行代码了，新建并编辑脚本 "~/.vim/vimmake.1"：

```python
#! /usr/bin/python
import sys, os

VIM_FILEDIR=os.environ.get('VIM_FILEDIR', '')
VIM_FILENAME=os.environ.get('VIM_FILENOEXT', '')

cmd = "cd \"%s\"; %s/%s; read -n1 -rsp press\ any\ key\ to\ continue\ ..."
cmd = cmd%(VIM_FILEDIR, VIM_FILEDIR, VIM_FILENAME)
cmd = cmd.replace('\\', '\\\\').replace('"', "\\\"").replace("'", "\\\'")
cmd = 'bash -c \"%s\"'%cmd

cmdline = 'gnome-terminal --command=\'%s\''%cmd
os.system(cmdline)
```

为了使用 Python 脚本来实现 '新窗口中运行程序'，我们需要用正确的参数来调用 gnome-terminal。把上面的脚本设置成 0755 以后记得 .vimrc里把工具 1 的启动模式设置成 bg: 

```text
let g:vimmake_mode['1']='bg'
```

运行模式 ‘bg' 的意思前面意境提到过，vimmake.1 这个 python脚本会在后台执行并且忽略任何输出（并不需要新版本vim支持，只是使用传统的 system('...&') 实现），这样你运行它时从vim的界面上就不会看到任何变化，只是弹出了我们需要的 gnome-terminal 窗口并运行给定的命令，当然你也可以设置成 async 模式，然后输出一行：xxxx 正在 running的文字到 quickfix窗口：

![](http://skywind3000.github.io/word/images/screen3.jpg)

嗯，这样把 `:VimTool 1` 命令 map 到 F6后，我们就可以在 ubuntu 的 vim 里直接 F6弹出新的 gnome-terminal 来跑我们的程序了，就和 Visual Studio 运行控制台程序一样，即便是长时间运行的程序，也不需要额外再开一个终端窗口，然后每次重新输入运行命令那么笨重。

在不同平台下（Windows, Cygwin, Ubuntu, Mac OS X）打开终端窗口运行特定命令是一件有点琐碎的事情，我写过一个脚本来专门干这事，或许对你有帮助：

[Skywind Inside - 如何在不同平台下打开新窗口运行程序？](http://www.skywind.me/blog/archives/1745)

有需要的话，可以把里面的 terminal.py 脚本复制到你的 vim 配置文件夹内，随时在 vim里打开新窗口运行程序。

---

如今 Vim 的异步任务机制已经很稳定，并且大部分系统自带的 Vim都已经高于 7.4.1829：

- FreeBSD 10自带的 Vim是 7.4.1832（请用 FreeBSD 的 pkg upgrade 更新到最新的 vim），
- Mac 上 brew可以更新到 7.4.1993，
- MacVim已经包含7.4.1831的版本，
- Windows下的 gvim 有每日最新的 Daily build （目前是 7.4.2032）
- Cygwin 的 vim 是 7.4.1999
- Debian 下 vim 是 7.4.576，需要自己编译一下最新版（注：1829已经进入test）。

----
上半年 vim async job 发布不久，我就试着给 vimmake 加入了 async 模式，随着4月份若干 job/channel 的边角问题被解决后，如今这部分功能已经很长时间没有碰到中等优先级以上的新bug了，我自己也用了三个月时间，觉得 vim 的异步机制如今完全可以一战了。

使用 vimmake 可以灵活的添加各种编译器运行工具，比单独为某种语言特化的插件灵活很多，我基本上把什么 SingleCompile, c.vim, vimgo 里类似的功能抛弃掉了，何况他们还不支持异步任务，你可以发挥你的想想用 vimmake 来做更多非编译运行的事情，比如 gvim 下编辑 html 的话，配置一下，一键直接打开 chrome 来显示当前的 html 文件之类的，或者调用 cppcheck来做静态代码检查，或者异步跑一个很大项目的 cscope 更新任务。

各位可以试试，喜欢的话，请为我在 http://vim.org 上投一票：
[vimmake - Customize shell tools for project building](http://www.vim.org/scripts/script.php?script_id=5418)
