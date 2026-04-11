---
uuid: 3671
title: 使用 rclone bisync 两步搭建个人云盘
status: publish
categories: 随笔
tags: Linux,网络
slug: 
date: 2026-01-30 00:27
---
如何最快搭建个人云盘？Nextcloud 太大太臃肿，后面一堆 apache/nginx/php/mysql，命令行同步也不好用，私货还太多。

著名的 syncthing 要求有 P2P 中转服务；还要求同步时另一台电脑也开着机，不开机的话，你要在服务器上做一个同步点持续运行，那么做了这个服务和 C/S 架构的 rclone 有啥区别呢？还要多依赖一个 P2P 中转服务（虽然可以找到别人提供的），其他的开源产品也好不到哪里，相比之下 rclone 是最轻量级的解决方案了。

恰巧 rclone 最近几年一直在优化 bisync 功能，就是双向同步，网盘的核心功能，bisync 在 2022 年引入 rclone 一直处于 experimental/beta 阶段，其实几年前就基本可以用了，官方文档在 2025 年下半年正式移除 experimental/beta 字样，然后 bisync 功能正式转正。

所以我们用 rclone 的 bisync 功能来分别搭建客户端和服务端：

1️⃣ 服务端搭建

使用 supervisor 编辑 `/etc/supervisor/conf.d/rclone-sftp.conf` 文件：

```ini
[program:rclone-sftp]
command=/home/data/app/rclone/rclone serve sftp /home/data/sync --addr :2022 --user MYNAME --pass MYPASS --cache-dir /var/cache/rclone --vfs-cache-mode full
user=nobody
autorestart=true
```

然后重启：

```bash
sudo supervisorctl reload
```

一个 rclone 提供的 sftp 服务就启动了，就是这么简单，它速度快性能好，传输有加密。

最后我们在 sftp 的文件夹里建立一个叫做 `bisync` 的文件夹：

```bash
sudo mkdir /home/data/sync/bisync
sudo chown -R nobody:nogroup /home/data/sync
```

处理好权限，让 `nobody` 这个用户能够读写即可，就这么几步操作，比搭建个 Nextcloud 之类的服务方便太多了。

2️⃣ 客户端

我用 WSL，编辑配置 `/root/.config/rclone/rclone.conf` 内容如下：

```ini
[sftp1]
type = sftp
host = 192.168.1.12
user = MYNAME
port = 2022
pass = [运行 rclone obscure "MYPASS" 得到的加密字符串]
shell_type = unix
md5sum_command = md5sum
sha1sum_command = sha1sum
```

不想手工填写也可以用 `rclone config` 交互式的初始化并连接 sftp 服务，一旦服务配置好了，我么就能找个文件夹然后在定时任务里 bisync 了。

<!--more-->

不过首先要初始化一下：

```bash
mkdir /mnt/e/Local/Cloud/rclone
rclone bisync /mnt/e/Local/Cloud/rclone sftp1:/bisync --resync
```

这个 `--resync` 参数用于首次同步初始化，后面就定时任务了。

编辑同步脚本 `/home/data/shim/rclone-bisync-sftp1` 内容如下：

```bash
#!/bin/bash

# configure
RCLONE_BIN="/home/data/app/rclone/rclone"
RCLONE_REMOTE=sftp1:/bisync
RCLONE_LOCAL=/mnt/e/Local/Cloud/rclone
LOGFILE="/var/log/rclone-bisync.log"

# start
$RCLONE_BIN bisync "$RCLONE_LOCAL" "$RCLONE_REMOTE" \
        --create-empty-src-dirs \
        --compare size,modtime \
        --resilient \
        --recover \
        --max-lock 2m \
        --verbose \
        --log-file="$LOGFILE"
```

定时启动：

编辑 `/etc/cron.d/rclone_bisync` 内容如下：

```text
*/5 * * * * root /home/data/shim/rclone-bisync-sftp1
```

即可，调试完正常可以把启动脚本里的 `--verbose` 去掉，没错误就不写日志了。你可以在多个客户端上进行类似的配置，不管 Windows 还是 Linux，要点就是先 config 上远端 sftp，然后初始化 `--resync`，然后就是定时调用 `bisync` 子命令就行。

然后你就得到了一个干净纯粹的，开源的，多端同步网盘了。


**后记**

在 bisync 之前，rclone 实现网盘主要靠 mount，这个功能类似 samba，每次读取写入都要走网络，局域网还行，跨机房就卡的不行了，它后来提供了 cache 机制有一定缓解，但一致性又有问题，经常不同步，这边改了不能像 samba 那样通知那边。

所以 rclone 做网盘体验最好的目前就是 bisync 功能了，bisync 的 bisync 可以用很多源，作为服务端，如果你不想搭建一大套 webserver / fileserver 来做源的话，最好就是用 rclone 自己可以 serve 的服务，包括：http，sftp，webdav，nfs 等等。

我试过 webdav 等，发现如果想要加密，前面还得再套一层 https 代理，或者又搞一大堆证书什么的，异常麻烦，所以体验最好，速度最快的是 sftp 服务。


