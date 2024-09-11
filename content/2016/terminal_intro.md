"=========== Meta ============
"StrID : 1745
"Title : 如何在不同平台下打开新窗口运行程序？
"Slug  : 
"Cats  : 随笔
"Tags  : Vim
"=============================
"EditType   : post
"EditFormat : Markdown
"TextAttach : vimpress_57347bf0_mkd.txt
"========== Content ==========
如果可以让自己的工作效率提升一点点，那么即便花费几天来开发一些工具也是值得的。在不同操作系统下自动打开终端窗口来运行指定的命令就是这样一件能提高工作效率的事情。

就像 Visual Studio 调试命令行程序的人都对打开一个新窗口运行命令行程序的模式情有独钟。EditPlus 也提供新窗口运行程序（可惜只限windows）。

而如果你在使用 Sublime/Atom/GEdit/GVim 之类的工具，你就会发现调试程序的时候程序基本上是在下面的面板中运行的，所有输出也是输出到下面的面板中。这时如果程序长时间运行是非常不方便的，又或者程序有交互（需要输入数据），基于GUI面板的运行方式也会显得十分笨重，而Vim/GVim之流更过分，一执行程序整个GUI就定住了，没法一边看代码一边查看一些长时间运行的程序状态，虽然Windows下的GVim可以用!start来解决（见[Gim !start](http://www.skywind.me/blog/archives/1708)），但十分遗憾，Linux桌面或者Mac下面的Vim都没有这个 !start功能。

同时，哪天你切换到Mac/Ubuntu下开发了，你会发现这个问题十分恶心，这时候你往往需要写一些脚本来做这件事情。而在不同的平台下正确的escape并传递参数，正确的生成中间脚本（bash，applescript，batch）并且通过管道传递又是一项比较浪费时间的事情。 

所以这两天写了: [https://github.com/skywind3000/terminal](https://github.com/skywind3000/terminal) 这个脚本来做这些，满足了我如下需求：

- 在 Windows 下打开 cmd窗口执行若干命令
- 在 Linux 下打开 xterm/gnome-terminal 来执行若干命令
- 在 Mac OS X 下面打开 Terminal/iTerm 窗口来执行若干命令
- 不同的操作系统下提供统一的调用接口
- 可以方便设置：工作目录、窗口标题、窗口配置（Terminal/gnome-terminal/iterm）
- 新窗口内执行完程序以后可以会等待按任意键才关闭窗口
- Windows 打开 Cygwin 的 Mintty窗口并执行 Cygwin命令（Windows下编辑，Cygwin下运行）
- Cygwin 下直接打开 Windows的 CMD窗口执行 Win32程序（Cygwin下编辑，Windows下运行）
- Cygwin 下直接打开 Mintty窗口并运行cygwin命令（Cygwin下编辑，cygwin下运行）

如此，不管你运行在哪个操作系统下，使用何种编辑器，都可以提供完全一致的调试体验。一边编辑代码的同时，一边查看另一个窗口的程序实时输出。

