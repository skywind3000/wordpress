"=========== Meta ============
"StrID : 1731
"Title : Vim异步编译工程
"Slug  : vim%e5%bc%82%e6%ad%a5%e7%bc%96%e8%af%91%e5%b7%a5%e7%a8%8b
"Cats  : 随笔
"Tags  : Vim
"=============================
"EditType   : post
"EditFormat : Markdown
"TextAttach : vimpress_57305917_mkd.txt
"========== Content ==========

针对 Vim的最新版本，7.4.1769+ 写了个脚本：[build.vim](https://github.com/skywind3000/vim/blob/master/asc/build.vim) 来实现异步编译。

主要实现原理是利用 Python 开线程并在后台线程调用脚本（具体执行编译工作的bat/sh文件），实时把stdout/stderr输出的内容投递到队列，而前台UI线程则是使用了Vim最新版本中提供的 timer_start 功能启动一个100ms运行一次的时钟，每次运行时检测队列里面的东西并把他们取出来输出到Vim的 Quickfix窗口。

几处细节处理是避免后台任务瞬间输出上千行的内容，批量塞入Quickfix的时候把vim 给卡死掉，此处增加了一个限制，即每次时钟发生时最大只塞入Quickfix中50条信息。

如此，整个世界清静了，以前Vim一编译代码就完全无法编辑的情况可以得到很好的解决了。你可以绑定<F1>-<F4>到外部命令：job-1 job-4 这四个不同的脚本（windows下是 job-1.cmd - job-4.cmd），用来执行外部命令，每次执行前，把当前编辑的文件名等信息写入环境变量，这样后台job-n.cmd的批处理就可以根据环境变量决定需要编译的文件或者工程信息了：

```text
let $VIM_FILEPATH = expand("%:p")
let $VIM_FILENAME = expand("%:t")
let $VIM_FILEDIR = expand("%:p:h")
let $VIM_FILENOEXT = expand("%:t:r")
let $VIM_FILEEXT = "." . expand("%:e")
let $VIM_CWD = expand("%:p:h:h")
let $VIM_RELDIR = expand("%:h")
let $VIM_RELNAME = expand("%:p:.")
let $VIM_CWORD = expand("<cword>")
let $VIM_VERSION = ''.v:version
let $VIM_MODE = ''. a:mode
let $VIM_GUI = '0'
let $VIM_SCRIPT = g:vimmake_path
let $VIM_SVRNAME = v:servername
if has("gui_running")
	let $VIM_GUI = '1'
endif

```

上面这些环境变量初始化工作可以在每次调用后台脚本之前设置，这几个应该已经足够大家使用了。

每次编译完还可以调用一下外部程序，播放一个音效（比如windows的感叹号音效），让你知道编译工作成功完成，方便你打开 Quickfix查看编译效果。


