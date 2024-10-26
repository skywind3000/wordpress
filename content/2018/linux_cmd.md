---
uuid: 3087
title: 有哪些命令行的软件堪称神器？
status: publish
categories: 随笔
tags: 命令行,神兵利器
slug: 
date: 2018-02-26 02:34
---
发几个好玩的玩具给大家新年玩玩：

⚡ **[cppman](https://github.com/aitjcize/cppman)：C++ 98/11/14 手册查询 for Linux/MacOS**

我知道你在 Windows 下有 Zeal ，你在 Mac OS X 用 Dash，但是你想在服务器上或者任意命令行环境下查看 C/C++ 语言手册么？偶尔看别人代码里调用到一个冷僻的 libc 函数（比如 strpbrk这种），网页搜索太慢，运行 zeal/dash 麻烦，想在命令行直接查看帮助怎么办？

这是个台湾小伙写的工具，使用很简单，跟 man一样，命令行输入：

```bash
cppman std::thread 
```

即可查看 thread 相关手册

![](https://skywind3000.github.io/images/blog/2018/cmd/cmd1.png)

可以配置到终端编辑器里设定个快捷键，一按下去就可以显示光标下面 token 的 reference，清晰的排版，美观的着色：

![](https://skywind3000.github.io/images/blog/2018/cmd/cmd2.png)

关键是速度快，比你开网页查便捷多了，

![](https://skywind3000.github.io/images/blog/2018/cmd/cmd3.png)

Windows 下用不了，可以在 WSL/MSYS/Cygwin 下面安装了一个，编辑器里照样一键弹出对应的帮助窗口，默认是在线请求 cppreference.com / cplusplus.com 的内容，可以花半小时一次性全部缓存到本地，提供离线帮助。

（点击 more/continue 继续）

<!--more-->


⚡ **[mcedit](https://midnight-commander.org)：终端下面的 NotePad++**

Windows 切换到 Linux 下工作，最缺的就是一款终端下趁手的编辑器，而如果你不想用 Vim/Emacs 的话，难道就只有用 nano 那么简陋的东西？或者 joe 这种奇葩的编辑器？有没有符合我 Windows 编辑习惯的趁手的终端编辑器呢？

有，mcedit （midnight commander 里面的一个工具）为你解决后顾之忧，快速安装：

```bash
apt-get install mc
```

或者 OS X 下：

```bash
brew install mc
```

即可安装 mc (midnight commander) 和 mcedit (mc internal editor)

这款编辑器如何？《[Debian 使用手册](https://qref.sourceforge.net/Debian/reference/ch-edit.zh-cn.html)》里作为最流行的编辑器，mcedit 就仅排在 vim和 emacs 之后；Debian 的 [官网 wiki](https://wiki.debian.org/TextEditor) 里，mcedit 亦是作为五款最好用的终端编辑软件之一推荐给大家。

不管是在终端下从事开发，还是链接到树莓派上改下配置，mcedit 将为你提供类似 NotePad++ 的编辑体验（按 `F9` 显示下拉菜单，或者鼠标点击第一行，或者 `ALT+F`）：

![](https://skywind3000.github.io/images/blog/2018/cmd/cmd4.png)

这款编辑器完全符合 NotePad++ 的编辑习惯：下拉菜单，多文件编辑+多子窗口管理，弹出对话框进行搜索/配置等，你记得住 Vim / Emacs 里复杂的查找替换规则么？mcedit里面不用记，UI上操作一切（知乎缩略图效果实在太糟糕了，请点击查看清晰大图）：

![](https://skywind3000.github.io/images/blog/2018/cmd/cmd5.jpg)

不需要学习任何配置文件格式，对话框里直接以UI的形式全部展现给你：

![](https://skywind3000.github.io/images/blog/2018/cmd/cmd6.jpg)

初次使用记得把设置里的 “visible tabs" 选项给干掉，它默认显示tab我觉得很丑。

你记得住 Emacs 的复制粘贴么？背得过来 Vim 那么多命令么？mcedit 不用背诵，它的帮助文档十分霸气，就一句话：“这个编辑器十分简单，不需要任何 手册和 tutor，要查看哪个键是干什么的，看看下拉目录就行了”，的确如此：

![](https://skywind3000.github.io/images/blog/2018/cmd/cmd7.png)

是不是很简单？不用看任何冗长的入门文档了？不会就鼠标点点点，什么都有了。连复制粘贴都是跟 NotePad++ 一样的 `SHIFT+方向键` 进行区域选择（想用鼠标拖？当然可以）。能同时打开多个窗口，任意切割窗口布局。

使用 NotePad++ 最方便的地方在于同开发工具链整合，能配置快捷键工具，`F1` 编译，`F2` 运行，对吧？ mcedit 决不让你失望，按 `F11` 弹出 User Menu：

![](https://skywind3000.github.io/images/blog/2018/cmd/cmd8.png)

上面是一些常用的代码片段，中间是编译运行选项，还有一些格式化，查询帮助等命令，这个 User Menu 针对不同的文件后缀展现不同的内容，关键是，完全可以配置，你可以使用各种宏配置你的程序的编译运行规则，配置入口在 Menu->Options->Menu File，当然，这里你需要写几行配置文件了，不过十分简单，可以参考已有的。

![](https://skywind3000.github.io/images/blog/2018/cmd/cmd9.png)

窗口管理也是贴合 Windows 的使用习惯，文件窗口可以任意覆盖，移动，最大化，堆叠。

默认使用鼠标即可，如果你想更高效点，可以研究下怎么再终端正确输入 ALT_X 按键。

怀旧的同志们也许还会想起以前的 Borland C++ 3.1，对吧？冲这点就赢得了我不少好感，说太多也没必要，基本都是鼠标点点点就知道大概的用法了，有这玩意儿，可以让你在 nano 和 vim/emacs 中间多一个负责任的选择。

⚡ **[icdiff](https://github.com/jeffkaufman/icdiff)：分屏显示 diff**

常规 diff：

![](https://skywind3000.github.io/images/blog/2018/cmd/cmd10.png)

icdiff：

![](https://skywind3000.github.io/images/blog/2018/cmd/cmd11.png)

比传统 diff 更明白些，是吧？效果比 sdiff 好不少，还可以配置到 git 里，变成默认的 git diff查看工具，比原来的 diff 漂亮不少吧？

⚡ **[z.lua](https://github.com/skywind3000/z.lua)：在 bash / zsh 中迅速切换项目目录**

他会跟踪你常去的目录，然后只需要你输入部分文件名就能正确跳转，终端下切换路径就像泥里走路，有了这个工具，能让你在终端下溜冰。

cd 到一个包含 foo 的目录：

```bash
z foo
```

cd 到一个以 foo 结尾的目录：

```bash
z foo$
```

对长路径使用多个关键字进行匹配：
假设路径历史数据库（~/.zlua）中有两条记录：

```
10   /home/user/work/inbox
30   /home/user/mail/inbox
```

"z in"将会跳转到 `/home/user/mail/inbox` 因为它有更高的权重，同时你可以传递更多参数给 z.lua 来更加精确的指明，如 "z w in" 则会让你跳到 `/home/user/work/inbox`。

详细使用见：[别让 cd 浪费你的时间](/blog/archives/2229)


⚡ **[cgasm](https://github.com/bnagy/cgasm)：命令行查询汇编指令**

Intel x86/x64 开发者手册，上千页的 PDF 里漫游，效率很低，对不对？cgasm 支持本地模糊搜索，比如查询 aes 相关的指令：

![](https://skywind3000.github.io/images/blog/2018/cmd/cmd12.png)

看 Intel 的 PDF 你要这么搞很费力吧？默认 cgasm + 指令，会显示简介。

![](https://skywind3000.github.io/images/blog/2018/cmd/cmd13.png)

当然，具体使用你会需要看更详细的说明，那么可以使用 cgasm -v aesenc，将会显示和开发手册 PDF里一致的内容：指令字节码，编码模式，状态影响，伪操作码描述和等价的 Intrinsic 等详细内容，比搜网页和查询 PDF效率高多了。

⚡ **[nextcloud](https://nextcloud.com)：DropBox 的开源替代品，提供命令行客户端 nextcloudcmd**

后端开发经常再不同的主机上跳来跳去，同步一些常用文件变得必不可少，当然你可以放到 DropBox 里，但我的 DropBox 账号只有一个，个人文件太多，不想再各种主机上乱放，且我发现 Linux 下的 DropBox 命令行客户端有时候会 100% cpu 占用，死循环了。

使用 nextcloud 当然要搭建公网服务端，这有一定门槛，但如果你有一台 vps 或者公网固定 ip 的服务器，可以用 docker 直接拉一个 nextcloud 服务器下来就行，五分钟都不到。作为 DropBox 的代替品 nextcloud 我很喜欢它一句口号：你的数据，你掌握。

把 nextcloudcmd 工具放到 crontab 里面，每五分钟对你的 ~/.cloud/ 目录进行一次同步，你直接修改一台机器上的 ~/.cloud/ 下面的文件，基本上一处修改，所有地方就及时自动同步上了，比用 git 同步常用资料方便多了。

⚡ **[ncdu](https://dev.yorhel.nl/ncdu)：可视化的空间分析程序**

你发现有人把 /home 空间撑爆了，影响了大家的工作，你愤怒了一层层的 du，一层层的 cd，整个过程就像刨垃圾堆一样的恶心，后来发现了 ncdu 这个基于 ncurses 的空间分析程序：

![](https://skywind3000.github.io/images/blog/2018/cmd/cmd14.png)

不但能用光标上下键移动，回车还可以进入对应目录又可以查看最新的占用，很快就揪出了占用空间最大的罪魁祸首。


⚡ **[glances](https://nicolargo.github.io/glances)：更强大的 htop / top 代替者**

htop 代替 top，glances 代替 htop：

![](https://skywind3000.github.io/images/blog/2018/cmd/cmd15.png)

信息比 htop 丰富了不少，更全了，对吧？除了命令行查看外，glances 还提供页面服务，让你从页面上随时查看某服务器的状态。

⚡ **[mc](https://midnight-commander.org) ：内容浏览/预览**

即便能舒适的呆在终端命令行里工作的人，有时候面对有些事情，也会感到烦躁，比如浏览一个目录的结构和里面文件内容，比如从源文件夹选择拷贝一批特定的文件到目标文件夹，这时候你需要 mc ，对就是前面 mcedit 的父项目 midnight commander ，安装方法同 mcedit：

![](https://skywind3000.github.io/images/blog/2018/cmd/cmd16.png)

和原来 Windows 下的 Total Commander 很类似，直接光标上下移动浏览文件，按 TAB键切换左右窗口，支持鼠标，支持内容预览，让你快速了解一堆文件夹里有些什么东西，按 F3 可以唤出 mcedit 预览文件，还可以用二进制查看文件内容，F4可以编辑文件。


⚡ **[ranger](https://github.com/ranger/ranger)：内容浏览/预览**

另一款内容预览软件，界面没有 mc 那么漂亮，标记拷贝也没它强，但是预览功能做的很不错，如果你习惯 vim 键位的话，你会发现 ranger 有些地方比 mc 顺手不少：

![](https://skywind3000.github.io/images/blog/2018/cmd/cmd17.png)

上下键（或者j, k）移动光标，内容预览自动出现在右边，左键可以回退上一层目录，q退出，如果你对预览很依赖，你会喜欢上 ranger 这款软件，apt-get 直接安装即可。


⚡ **[dstat](http://dag.wiee.rs/home-made/dstat)：vmstat 代替者**

可能不少人都用过，但是本问题下好像没人提？

![](https://skywind3000.github.io/images/blog/2018/cmd/cmd18.png)

能输出比 vmstat 更加：美观，整洁，强大的内容。


⚡ **[cheat](https://github.com/cheat/cheat)：命令行笔记**

就是各种 cheat sheet ，比如经常搞忘 redis 命令的话，你可以新建 ~/.cheat/redis 这个文件，写一些内容，比如：

```bash
cat /etc/passwd | redis-cli -x set mypasswd
redis-cli get mypasswd
redis-cli -r 100 lpush mylist x
redis-cli -r 100 -i 1 info | grep used_memory_human:
redis-cli --eval myscript.lua key1 key2 , arg1 arg2 arg3
redis-cli --scan --pattern '*:12345*'
```

然后使用的时候，cheat redis 命令就可以显示出来刚才新建的 cheat sheet 了：

![](https://skywind3000.github.io/images/blog/2018/cmd/cmd19.png)

同样 cheat 本身还自带了很多常用 cheat sheet，比如你可以试试：

```bash
cheat tar      # 当你忘记 tar 命令时候
cheat vim      # vim cheat sheet
cheat rsync    # 文件同步的 cheat sheet
```

忘记 Vim 怎么退出了？没关系 cheat vim 就可以显示 vim cheat sheet 了，对于一些重要的，但是不常用的，经常搞忘的东西，特别有用，比如我最痛恨的 https + svn 搭建过程，第一次查资料弄好，然后忘了，半年后又要再弄时又得全部重新查找资料，然后又忘记了，有了这个就比较好办。

再比如 rsync 的用法，我就老记不住，man rsync 又是废话连篇不着重点，看它自带的 cheat 效率提高不少，注意时常更新，作者会不断添加 cheat sheet。

这显然比你查询网页开 evernote 效率来的快，使用环境变量 DEFAULT_CHEAT_DIR 可以设定 ~/.cheat 以外的个人 cheat 目录，一般很多人都会在 github 上建立一个个人配置文件的项目，里面放满自己的 vim / zsh / bash 等配置，现在可以把个人 cheat 文件也纳入这个项目的管理，这样你就比较方便的能在不同的机器上同步你自己建立的各种 cheat sheet 了。

随着你自定义了越来越多的 cheat sheet，你的工作效率会变得越来越高。

⚡ **[multitail](https://www.vanheusden.com/multitail)：多重 tail**

通常你不止一个日志文件要监控，怎么办？终端软件里开多个 tab 太占地方，可以试试这个工具：

![](https://skywind3000.github.io/images/blog/2018/cmd/cmd20.png)

上面演示了同时监控两个日志文件，有高亮显示不同内容，当然还可以同时监控更多日志：

![](https://skywind3000.github.io/images/blog/2018/cmd/cmd21.png)

也许你会问，这和 tmux + tail 有什么区别？区别大了，multitail 可以做太多 tmux + tail 做不了的事情了，比如：

- 日志色彩高亮
- 窗口自动管理，自动调整大小。
- 多个日志文件窗口可以合并到一个里面，就像一个 log 文件一样查看。
- 临时显示/隐藏某个日志文件窗口。
- 可以对所有日志文件进行同一关键字搜索。
- 日志过滤，外部正则表达式工具分析。
- 众多常见服务的日志高亮模板，如：tcpdump，apache，squid，strace

等等，自己到它主页看吧，比 tmux + tail 强多了，操作也比 tmux 方便。


⚡ **[bro](http://bropages.org)：以用例为主的帮助系统**

man 以外的帮助系统有很多，除去 cheat, tldr 外，还有一款有意思的帮助系统 -- bro，它是以用例为主的帮助，所有用例都是由用户提供，并且由用户投票筛选出来的：

![](https://skywind3000.github.io/images/blog/2018/cmd/cmd22.png)

比如我们查看 cut 命令的帮助，就运行 “bro cut”，显示内容如图，查看按投票多少排序，你如果觉得哪条解释比较好，你可以投赞成票，或者反对票。

安装很简单，先安装 ruby 和 ruby-dev ，然后：

```bash
gem install bropages
```

即可，相比由某些官方写的帮助文档，这种知乎式的帮助筛选方法，更容易将最好的帮助信息筛选出来。

--

相关阅读：

[终端调试哪家强？](/blog/archives/2036)

[为什么说 zsh 是 shell 中的极品？](/blog/archives/2060)

[有哪些好用的 bash 技巧（包括不限于快捷键、自用小脚本）？](/blog/archives/2071)

