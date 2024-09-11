---
uuid: 2534
title: WSL 服务自动启动的正确方法
status: publish
categories: 未分类
tags: 命令行
date: 2018-10-26 14:22
slug: 
---
2018年 Windows 10 下的 WSL 已经可以保留后台进程了，从此后，用了十多年的 cygwin 基本失去了存在的价值了。网上有很多 WSL 自动启动服务的方法，但是都有些大大小小的问题，很多又是针对最老的 ubuntu16.04 发行版（输入 bash启动哪个），你如用商店里下载的最新的 WSL 版本 Debian9/Ubuntu18.04 就会出错。

所以正确在 WSL 里自动启动服务的方式有必要记录一下。

创建启动脚本：

进入任意 WSL 发行版中，创建并编辑文件：/etc/init.wsl

```bash
#! /bin/sh
/etc/init.d/cron $1
/etc/init.d/ssh $1
/etc/init.d/supervisor $1
```

里面调用了我们希望启动的三个服务的启动脚本，设置权限为可执行，所有者为 root，这时候可以通过：

```bash
sudo /etc/init.wsl [start|stop|restart]
```

来启停我们需要的服务，接着在 Windows 中，开始-运行，输入：

```
shell: startup
```

按照你 WSL 使用的 Linux 发行版创建启动脚本，比如我创建的 Debian.vbs 文件：

```vbs
Set ws = CreateObject("Wscript.Shell")
ws.run "wsl -d debian -u root /etc/init.wsl start", vbhide
```

这个脚本就会在你登陆的时候自动在名字为 "debian" 的 wsl 发行版中执行 /etc/init.wsl 启动我们的服务了，如果你用的是 ubuntu18.04 的发行版，那么修改上面脚本里的 debian 为 ubuntu1804.vbs：

```vbs
Set ws = CreateObject("Wscript.Shell")
ws.run "wsl -d Ubuntu-18.04 -u root /etc/init.wsl start", vbhide
```

而如果你不知道自己的 WSL 发行版叫做什么名字，可以用 “wsl -l" 来查看。不管你用最初的 bash (ubuntu 16.04) 还是商店里下载的 debian/ubuntu1804 都能顺利启动服务了。

WSL 中有很多有用的服务，你可以按需删改 /etc/init.wsl ，但没必要塞很多东西进去影响你的启动速度，比如 mysql/mongodb 这些重度服务，可以需要的时候再启动，用完就停了。

我自己用的比较多的服务就三个：sshd（启动了以后支持终端软件登陆wsl，像远程服务器一样操作），supervisord（用于托管其他服务，比如 ssr），crond（crontab，自由定制定时任务），大部分时候，用上面三个足以。
