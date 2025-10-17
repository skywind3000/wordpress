---
uuid: 2229
title: 别让 cd 浪费你的时间
status: publish
categories: 随笔
tags: 命令行
date: 2019-02-27 23:37
---
终端下工作最烦躁的就是路径切换，没有自动路径切换的帮助，就像在泥里走路，于是有了各种 autojump / z / fasd 等工具来提升路径切换的效率，今天向大家介绍一个更好用的工具：[z.lua](https://github.com/skywind3000/z.lua)，用熟练了以后就像终端里溜冰，路劲切换从此指哪打哪。

[z.lua](https://github.com/skywind3000/z.lua) 是一个会学习你使用习惯的 `cd` 命令，它会跟踪你在 shell 下访问过的路径，通过一套称为 Frecent 的机制（源自 Mozilla），经过一段简短的学习之后，`z.lua` 会帮你跳转到所有匹配正则关键字的路径里 Frecent 值最高的那条路径去。

正则将按顺序进行匹配，"z foo bar" 可以匹配到 /foo/bar ，但是不能匹配 /bar/foo。

#### 特性说明：

- 性能比 **z.sh** 快三倍，比 **fasd** / **autojump** 快十倍以上。
- 支持 Posix Shell：bash, zsh, dash, sh, ash, busybox 等等。
- 支持 Fish Shell，Power Shell 和 Windows cmd。
- 使用增强匹配算法，更准确的带你去到你想去的地方。
- 低占用，能够仅在当前路径改变时才更新数据库（将 `$_ZL_ADD_ONCE` 设成 1）。
- 交互选择模式，如果有多个匹配结果的话，跳转前允许你进行选择。
- 交互选择模式，支持使用 fzf 进行可视化结果筛选（可选）。
- 快速跳转到父目录，或者项目根目录，代替反复 “cd ../../.." 。
- 为不同的操作系统，不同的 Shell 程序提供统一的使用体验。
- 兼容 lua 5.1, 5.2 和 5.3 以上版本。
- 自包含且无额外依赖，单个 `z.lua` 文件完成所有工作。

#### 软件安装：

将下面对应语句添加到你的 `.bashrc` / `.zshrc` / `.profile` 或者对应 shell 的初始化脚本末尾：

```bash
eval "$(lua /path/to/z.lua --init bash enhanced once echo)"    # BASH 初始化
eval "$(lua /path/to/z.lua --init zsh enhanced once echo)"     # ZSH 初始化
eval "$(lua /path/to/z.lua --init posix enhanced once echo)"   # 其他 Posix Shell 初始化
source (lua /path/to/z.lua --init fish enhanced once echo | psub)  # Fish Shell 初始化
iex ($(lua /path/to/z.lua --init powershell enhanced once echo) -join "`n") # Power Shell 初始化
```

然后重新登陆，即可使用。

#### 用户评价：

“我喜欢它的原理，我在命令行下面的行为十分有规律，并且我十分懒惰，懒得管理和维护一套书签或者路径别名。“

“总之，z.lua 做到了它所宣称的目标。如果你需要快速的在目录间切换，它可能是最好的选择。“

”我终于可以在自己的树莓派1上使用 autojump 类似的功能了，而不用像以前传统 autojump 那样每次打开终端都要等待 30 秒。”

#### 基本使用：

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

"z in"将会跳转到 /home/user/mail/inbox 因为它有更高的权重，同时你可以传递更多参数给 z.lua 来更加精确的指明，如 "z w in" 则会让你跳到 /home/user/work/inbox。

#### 交互选择：

使用 -i 参数进行跳转时, 如果有多个匹配结果，那么 z.lua 会给你显示一个列表：

```bash
$ z -i soft
3: 0.25   /home/data/software
2: 3.75   /home/skywind/tmp/comma/software
1: 21     /home/skywind/software
> {光标位置}
```

然后你按照最前面的序号输入你想要去的地方，比如输入 3 就会进入 `/home/data/software`。如果你不输入任何东西直接按回车，那么将会直接退出而不进行任何跳转。

PS：交互选择同时支持 "-I" 参数（大写 i），让你可以使用 fzf 在多项结果进行快速选择（如果系统里面安装了的话）。

#### 快速回到父目录：

"-b" 选项可快速回到某一级父目录，避免重复输入 "cd ../../.."，一般把 "z -b" 别名成 "zb" 命令：

- （没有参数）：cd 到项目根目录，即跳转到父目录中包含 (.git/.svn/.hg) 的地方。
- （单个参数）：cd 到最近一级以关键字开头的父目录中。
- （两个参数）：对当前目录进行字符串替换，然后 cd 过去。

使用举例：

```bash
# 一直向上退到项目根目录（就是里面有一个 .git 目录的地方）
~/github/lorem/src/public$ zb
  => cd ~/github/lorem

# cd 到第一个以 g 开头的父目录
~/github/vimium/src/public$ zb g
  => cd ~/github

# 快速回到 site 目录
~/github/demo/src/org/main/site/utils/file/reader/whatever$ zb si
  => cd ~/github/demo/src/org/main/site

# 将 jekyll 替换为 ghost
~/github/jekyll/test$ zb jekyll ghost
  => cd ~/github/ghost/test
```

向后跳转同样也支持环境变量 `$_ZL_ECHO`（用来显示跳转结果），这样为搭配其他工具提供了可能性（并不需要改变当前工作目录）：

```bash
# 假设我们位于 ~/github/vim/src/libvterm
# 打开 $_ZL_ECHO 用于在每次跳转后调用一次 pwd 显示当前目录
$ _ZL_ECHO=1

# 看看我项目根目录（有 .git 那个）目录里有什么？
$ ls -l `zb`
  => ls -l ~/github/vim

# 检查 "<项目根目录>/logs" 下面的日志
$ tail -f `zb`/logs/error.log
  => tail -f ~/github/vim/logs/error.log

# 查看一下某一级父目录里有些啥
$ ls -l `zb git`
  => ls -l ~/github
```

**Bonus**：“zb ..” 相当于 “cd ..”，“zb ...” 相当于 “cd ../..”，而 “zb ....” 相当于 “cd ../../..” 等等。 最后 “zb ..20” 等同于调用 “cd ..” 二十次。

#### 常用技巧：

推荐一些常用别名，放在你的配置文件中：

```bash
alias zc='z -c' # 严格匹配当前路径的子路径
alias zz='z -i' # 使用交互式选择模式
alias zf='z -I' # 使用 fzf 对多个结果进行选择
alias zb='z -b' # 快速回到父目录
```

z.lua 可以方便的导入 z.sh 的数据（他们格式相同）：

```bash
cat ~/.z >> ~/.zlua
```

还可以导入 autojump 的数据：

```bash
FN="$HOME/.local/share/autojump/autojump.txt"
awk -F '\t' '{print $2 "|" $1 "|" 0}' $FN >> ~/.zlua
```

更多内容，参考项目文档：

[https://github.com/skywind3000/z.lua](https://github.com/skywind3000/z.lua)

