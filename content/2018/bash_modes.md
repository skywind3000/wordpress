---
uuid: 3053
title: 千万别混淆 Bash/Zsh 的四种运行模式
status: publish
categories: 随笔
tags: 命令行,Linux
slug: 
date: 2018-11-17 03:35
---
Bash/Zsh 有四种不同运行模式，你的 bash 配置写错地方的话，不但会拖慢 bash 的速度，还会发生明明写了登陆配置但是就是没生效的情况。

#### 第一个维度：interactive mode / non-interactive mode

Bash 的 _交互模式（interactive mode）_ 是指你直接输入：

```bash
bash
```

以后 bash 出现一个 "`$> `" 的 PROMPT，等待用户不断的输入指令，输入 "exit" 或者按了 CTRL+D 才会结束。你 ssh 登陆到一台电脑，或者命令行下面打 bash ，后面没有参数的话，进入的都是交互模式。

而 _非交互模式（non-interactive mode）_ 是指你用 bash 运行一个命令或者脚本，运行完 bash 就退出那种：

```bash
bash -c "echo 123"
bash script.sh
```

上面这两种情况下，bash 运行完脚本，就退出了，不会出现 PROMPT，也不会等待用户输入新指令。

境变量 `$-` 里如果有字符 i 的话，代表是一个 interactive shell，否则是 non-interactive mode，我们可以简单测试一下：

```bash
$> [[ $- == *i* ]] && echo "Interactive" || echo "Not interactive"
Interactive
$>  bash -c '[[ $- == *i* ]] && echo "Interactive" || echo "Not interactive" '
Not interactive
```

登陆过后的 shell 都是交互模式的，再交互模式下直接检测 `$-` 得到 "Interactive" 的结果，而bash 直接运行命令属于非交互模式，所以输出 "Not interactive"

再写一个脚本：`check_interactive.sh` 继续验证：

```bash
#! /bin/bash
[[ $- == *i* ]] && echo "Interactive" || echo "Not interactive"
```

检验一下：

```bash
$> source check_interactive.sh
Interactive
$> bash check_interactive.sh
Not interactive
$> bash -c "source check_interactive.sh"
Not interactive
```

在 Bash 中，`source <文件名>` 是在当前 bash shell 进程内执行脚本，效果和直接敲里面的命令一样，所以是交互模式。而 `bash <文件名>` 是启动一个新的 bash 进程执行脚本，所以是非交互模式。

因此，我们平时写的一大堆 bash 配置，都是针对 “交互模式” 的，如果让 bash 执行条命令都要去运行各种初始化脚本的话，效率太低了，所以 `~/.bashrc` 开头就有一句判断：

```bash
# If not running interactively, don't do anything
[[ "$-" != *i* ]] && return
```

或者写为：

```bash
# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac
```

就是为了避免非交互模式随便运行一条命令都要解析后面的各种配置用的。

当然，新版本的 bash 如果以非交互模式启动，会直接跳过 `~/.bashrc` 的解析，而这几行 bashrc 中的检测为了兼容被保留了下来。

因此，如果我们不确定 bash/zsh 的版本和行为，又自己从头开始写配置的话，需要在配置开头增加相应的检测代码，避免不必要的工作。

（点击 more/continue 继续）

<!--more-->

#### 第二个维度：Login shell / Non-login shell

前面的 `交互模式` 与 `非交互模式` 区别的是 bash/zsh 用于接受用户命令，还是执行运行一段脚本。 而这里的 “登陆 shell” 和 “非登陆 shell”决 定的是 bash 加载哪个登陆脚本：

- 登陆 shell：终端登陆时，ssh链接时，`su --login <username>` 切换用户时。
- 非登陆 shell：直接运行 bash 时，`su <username>` 切换用户时（前面没有加 --login）。

使用下面命令可以判断当前模式：

```bash
shopt -q login_shell && echo "Login shell" || echo "Not login shell"
```

我们测试一下：

```bash
$> shopt -q login_shell && echo "Login shell" || echo "Not login shell"
Login shell
```

如果你才登陆，运行上面命令会显示 “Login shell” 而如果你不是登陆过来的，而是 su 切换到某用户再运行，就会显示 "Not login shell"。如果你 su 的时候加了 --login 参数的话，又会和你登陆是一样的。

进入 bash 交互模式时也可以用 --login 参数来决定是否是登陆模式：

```bash
$> bash
$> shopt -q login_shell && echo "Login shell" || echo "Not login shell"
Not login shell
$> exit
$> bash --login
$> shopt -q login_shell && echo "Login shell" || echo "Not login shell"
Login shell
$> exit
```

上面两次进入 bash 交互模式，由于后面加了 --login，所以检测的结果都不相同。再测试非交互模式下的区别：

```bash
$> bash -c 'shopt -q login_shell && echo "Login shell" || echo "Not login shell"'
Not login shell
$> bash --login -c "shopt -q login_shell && echo "Login shell" || echo "Not login shell"'
Login shell
```

直接运行命令的非交互模式也有这两种模式，因此交互/非交互，login/not login 是正交的一共四种模式。

那么 bash 在登陆和非登陆状态下具体行为有和不同呢？答案是初始化脚本不同：

- 非登陆模式：只加载 `~/.bashrc`，加载完就继续了。
- 登陆模式：只加载 `~/.bash_profile`，加载完就继续了，除非 `~/.bash_profile` 不存在，那么尝试加载 `~/.bashrc`，然后再继续。
  
所以如果你的系统里面如果只有一个 `~/.bashrc` 文件，那么不论哪种模式它都会被加载。而如果你系统中同时存在 `~/.bashrc` 和 `~/.bash_profile` 的话，就会根据是否 login shell 而选择性加载前者和后者了。

那么这里也许有人要问，搞那么复杂干嘛？一个配置就行了嘛，其实是有必要的，当你登陆时，比如你可以在脚本里检测只有登陆时才做一些事情：

- 检查 mailbox
- 显示欢迎语句
- 记录登陆日志之类

也就是 ssh 连到服务器上，显示一大串欢迎。

比如我的 bash 配置里就检测了如果是 login shell 的话，随机显示一则 debian 使用技巧，这样每次我 ssh 到服务器上，都能看到一则技巧提示，而我 su 切换用户，或者直接运行 bash 的时候却不用显示，除非加上了 --login 参数。

![](https://skywind3000.github.io/images/blog/2018/bash_modes.jpg)

上面还可以看得出来，login shell 下可以用 logout 或者 exit 退出，而 non-login shell 下面，则只能使用 exit 退出。

因此判断是否是 login shell 也是配置 bash/zsh 的基本问题，正确的区分两种模式，可以给真正登陆的用户在登陆前显示更多有用的提示语或者执行某些初始化命令，而登陆过后使用普通 su 切换用户的时候却可以跳过这些步骤。

补充一下，如果你使用 zsh 的话，没有 shopt 命令，需要通过：

```bash
[[ -o login ]] && echo "Login shell" || echo "Not login shell"
```

来判断，现在的系统一般都没有 `~/.bash_profile` 文件了，只保留 `~/.bashrc` 文件，但是如果你新建 `~/.bash_profile` 的话，还是会导致登陆时 `~/.bashrc` 被跳过，所以有的系统里，`~/.bash_profile` 只有简单的一段：

```bash
# login shell will execute this
if [ -n "$BASH_VERSION" ]; then
	# include .bashrc if it exists
	if [ -f "$HOME/.bashrc" ]; then
		. "$HOME/.bashrc"
	fi
fi
```

就是避免登陆时 `~/.bashrc` 被跳过的情况。

所以当系统里同时存在 `~/.bash_profile` 和 `~/.bashrc` 的时候，你如果把一些 alias 的配置写到了 `.bash_profile` 里，你就会发现只有登陆该用户的时候才会生效，而 su 过去时，完全无法使用，因为 su 时 `.bash_profile` 被跳过了。

所以如果你想让一些 alias 不管登不登陆都生效的话，请写到 `.bashrc` 文件里，然后确保 `.bash_profile` 中也会加载 `.bashrc` 文件，或者直接删除 `.bash_profile` 配置文件，只保留 `.bashrc` 即可。

至于 zsh ，两种模式解析的都是 `~/.zshrc` ，所以需要你自己再 `~/.zshrc` 中判断情况。

最后配一张插图：（侵删）

![](https://skywind3000.github.io/images/blog/2018/bash_startup.png)

相关说明：

```text
/etc/profile
       The systemwide initialization file, executed for login shells
~/.bash_profile
       The personal initialization file, executed for login shells
~/.bashrc
       The individual per-interactive-shell startup file
~/.bash_logout
       The individual login shell cleanup file, executed when a login shell exits
~/.inputrc
       Individual readline initialization file
```

那么看到这里，你的 bash/zsh 配置写对了么？是否可以再优化一下？
