---
uuid: 2828
title: EditPlus 的配置方法
status: publish
categories: 未分类
tags: 神兵利器
slug: 
date: 2024-09-05 23:05
---
作为一名编辑器爱好者，EditPlus 是我最喜欢的编辑器之一，超过 NotePad++，它启动速度比它快，打开文件比它快，功能比它强，颜值也比它高，但大小只有 2MB：

![](https://skywind3000.github.io/images/blog/2024/epp/editplus.png)

用了这么多年，我感觉我欠 EditPlus 一篇文章，介绍一下我平时是如何是用 EditPlus 搭建开发环境的，以及如何让它变得更好用：

（点击 more/continue 展开）

<!--more-->

先配置下 GCC 的工具，选择主菜单 Tools-> Configure User Tools：

![](https://skywind3000.github.io/images/blog/2024/epp/tool1.png)

然后点右边按钮 “Add Tool” 并选择 “Program”，然后在下面填空：

```text
Menu text: Execute Program
Command: C:\Windows\system32\cmd.exe
Argument: /C "$(FileNameNoExt)"
Initial directory: $(FileDir)
```

这些形如 `$(FileDir)` 之类的宏不用死记，点输入框右边的下箭头按钮，就能弹出菜单，让你选择后自动插入：

![](https://skywind3000.github.io/images/blog/2024/epp/menu1.png)

配置好以后，点下方 “Apply” 按钮确定，这样我们多出一个工具来，按 Ctrl+1 运行当前 C++ 程序；继续添加一个编译工具，接着点击 “Add Tool” 选择 “Program”，填写如下内容：

![](https://skywind3000.github.io/images/blog/2024/epp/tool2.png)

具体内容：

```text
Menu text: GCC Compile
Command: D:\Dev\mingw\bin\gcc.exe
Argument: "$(FileName)" -o "$(FileNameNoExt)"
Initial directory: $(FileDir)
```

注意文件名用引号括号，防止带空格的文件名出错，其次下方的 “Action” 选择 “Capture output”，这样就不会弹出新的 cmd 窗口运行，而是将输出捕获到下方面板，并且匹配输入错误，设置好按 OK。

![](https://skywind3000.github.io/images/blog/2024/epp/tools.png)

这样在主目录的 Tools 菜单下面，就出现了两个新配置的用户工具，分别按 Ctrl+1 和 Ctrl+2 运行，比如我们先按 Ctrl+2：

![](https://skywind3000.github.io/images/blog/2024/epp/tool3.png)

编译当前文件，因为没啥输出，所以下面的面板也没啥内容，注意有的 MinGW 环境可能需要你把他的 `bin` 目录设置到 `PATH` 环境变量中，你可以设置个全局的，编译成功后再按 Ctrl+1 运行程序：

![](https://skywind3000.github.io/images/blog/2024/epp/tool4.png)

运行程序因为没有捕获输出，所以是弹出终端窗口运行的，而且运行完会提醒你按任意键继续，一般编译器调用这种有错误输出的，都是配置成捕获输出，让错误在下面显示，比如故意把程序改错再编译一次：

![](https://skywind3000.github.io/images/blog/2024/epp/tool5.png)

下面显示了错误，并且支持鼠标双击就跳转到具体位置，这样一套简易的 C++ 开发环境搭建成功了，照葫芦画瓢，再配置一个 Python 运行工具：

![](https://skywind3000.github.io/images/blog/2024/epp/tool6.png)

这样按 Ctrl+3 就可以运行当前 Python 脚本，类似的方法，还可以将 GNU Make / CMake 之类的工具配置进去，无外乎把 `$(FileDir)` 换成 `$(ProjectDir)` 代表项目目录，或者 `$(DirWin)` 代表左边文件树的根目录。

配置好工具以后，在配置一些快捷键，继续在这个配置窗口选择左边 Tools 下面的 Keyboard 选项：

![](https://skywind3000.github.io/images/blog/2024/epp/keyboard.png)

右边 Types 列表选择 Window，然后 Commands 选择 Window1，然后在下面 Press new shortcut 的地方点下鼠标，然后按 ALT+1，再点右边的 Assign 按钮：

![](https://skywind3000.github.io/images/blog/2024/epp/keyboard2.png)

这样就可以用 ALT+1 时切换到第一个标签页的文件，同理把 Window2 到 Window9 赋给 ALT+2 到 ALT+9，以及 Windows10 赋给 ALT+0，这样当同时打开多个文件的时候 ALT+Num 进行快速切换。

不过文件多的时候也可以用主菜单 Window -> Window List (Shift+F12) 来显示窗口列表，供你快速切换：

![](https://skywind3000.github.io/images/blog/2024/epp/fuzzy.png)

并且提供模糊搜索功能，敲入部分文件名就能快速筛选，类似 VS 里的 VAX 红番茄插件的 Alt+shift+o 功能。

最后调整下支持的语言，还是 Tools -> Preference 窗口，左边分类那里选择 File 下面的 Settings & Syntax 然后中间文件类型选择 C/C++：

![](https://skywind3000.github.io/images/blog/2024/epp/cpp.png)

然后把下面 Auto Completion 前面的勾去了，如果不喜欢它奇怪的补全系统的话，进一步的话，新增一些语言，到 EditPlus 官网的 User Files 上去下载一些语法文件设置上去，比如 cmake 之类的，增加下新的语法高亮。

基本设置差不多就这些，这样应该比之前好用不少了。

**技巧1：运行时自动检测文件类型**

Q：之前运行 C 代码配置到 Ctrl+1 上，而 Python 运行配置到 Ctrl+3 上了，如果还有其他语言，有没有办法将多种语言的运行共用一个快捷键？

A：可以的，建立个 launch.cmd 批处理文件：

```
@echo off
if "%1" == "" GOTO EXIT

if "%~x1" == ".c" call "%~n1"
if "%~x1" == ".cpp" call "%~n1"
if "%~x1" == ".cc" call "%~n1"
if "%~x1" == ".cxx" call "%~n1"
if "%~x1" == ".py" python "%1"
if "%~x1" == ".pyw" pythonw "%1"
if "%~x1" == ".pl" perl "%1"
if "%~x1" == ".lua" lua "%1"

:EXIT
```

它会判断扩展名并使用适当的方式来运行，修改下之前配置的 Execute Program 这个工具：

```text
Menu text: Execute Program
Command: C:\Windows\system32\cmd.exe
Argument: /C D:\Path\to\launch.cmd "$(FileName)"
Initial directory: $(FileDir)
```

就行了，使用 launch.cmd 去执行你的当前文件，然后 Ctrl+1 会自动判断类型并执行。

**技巧2：不想把 MinGW 的 bin 目录设置到全局怎么办？**

Q：假设有三四套 MinGW，不想将他们设置到全局 `PATH` 想避免冲突该怎么办呢？
A：写一个 mingw32.cmd 的批处理包裹以下即可：

```
@echo off
setlocal enabledelayedexpansion
set "PATH=d:\path\to\mingw\bin;%PATH%"
IF NOT "%1" == "" call %*
endlocal
```

注意将 `d:\path\to\mingw\bin` 改成具体的值，这个批处理会在局部设置 `PATH` 然后调用玩工具后又恢复，然后使用时用：

```bash
mingw32 gcc --version
```

就相当于设置好 `PATH` 再调用：

```bash
gcc --version
```

不会污染到外面的环境。

还可以更进一步，假设你在 D:\\ 下面有 MinGW32 和 MinGW64 两套工具链，你可以只写一个 mingw.cmd 放到各自目录下：

```
@echo off
setlocal enabledelayedexpansion
set "PATH=%~dp0bin;%PATH%"
IF NOT "%1" == "" call %*
endlocal
```

两个目录里面各自放一个上面的 mingw.cmd 文件，然后用各自目录下的 mingw.cmd 启动工具，就能设置对应 mingw.cmd 所在目录的 bin 子目录进入 PATH，不用每个 mingw 环境写一遍了。

然后新建个 MinGW 的工具：

![](https://skywind3000.github.io/images/blog/2024/epp/mingw32.png)

具体配置：

```text
Menu text: MinGW32
Command: D:\Path\to\mingw32\mingw.cmd
Argument: gcc "$(FileName)" -o "$(FileNameNoExt).exe"
Initial directory: $(FileDir)
```

记得把 Action 设置成 Capture output 然后点击 Apply 按钮即可，此时按 Ctrl+4 激活这个 MinGW32 环境，又不需要外层去改 `PATH` 环境变量。

**技巧三：函数列表**

Q：如何在文档中间进行快速跳转呢？
A：如果要不停的切换文件编辑，那左侧就开着文件树，而如果长时间编辑一个文件的话，左侧可以切换到 Function （函数列表）功能：

![](https://skywind3000.github.io/images/blog/2024/epp/function.png)

点击左侧的函数可以进行快速跳转，上方输入框可以进行模糊匹配。

**技巧4：CMake 文件类型**

有同学反馈从 editplus 官网下载了 cmake 语法文件，设置成新的文件类别后不识别，会被识别成 `.txt` 的普通文本文件。

这里有两个关键点，第一是新建了 CMake 类型后，不要填写 File extensions，而是点右边的 "Advanced" 按钮：

![](https://skywind3000.github.io/images/blog/2024/epp/cmake.png)

然后填写 "An additional file name" 为 "CMakeLists.txt" 文件名，然后 OK；第二步是回到文件类型设置窗口，将新建的 CMake 文件类型用 "Up" 按钮，往前移动，移动到 Text 类型前，这样在检测 Text 类型之前，"CMakeLists.txt" 就能被提前检测出来，不会再被 Text 类型识别成普通文本文件。


好了，到这里你已经是一个 EditPlus 的 Pro 用户了。
