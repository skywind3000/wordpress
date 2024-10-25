---
uuid: 2641
title: 用好你的瑞士军刀/netcat
status: publish
categories: 网络编程
tags: 网络,命令行
slug: 
date: 2019-09-24 22:12
---
Netcat 号称 TCP/IP 的瑞士军刀并非浪得虚名，以体积小（可执行 200KB）功能灵活而著称，在各大发行版中都默认安装，你可以用它来做很多网络相关的工作，熟练使用它可以不依靠其他工具做一些很有用的事情。

最初作者是叫做“霍比特人”的网友 Hobbit <hobbit@avian.org> 于 1995 年在 UNIX 上以源代码的形式发布，Posix 版本的 netcat 主要有 GNU 版本的 netcat 和 OpenBSD 的 netcat 两者都可以在 debian/ubuntu 下面安装，但是 Windows 下面只有 GNU 版本的 port。

不管是程序员还是运维，熟悉这个命令都可以让很多工作事半功倍，然而网上基本 90% 的 netcat 文章说的都是老版本的 OpenBSD 的 netcat，已经没法在主流 linux 上使用了，所以我们先要检查版本：

在 debian/ubuntu 下面：

```bash
readlink -f $(which nc)
```

看看，结果会有两种：

- `/bin/nc.traditional`: 默认 GNU 基础版本，一般系统自带。
- `/bin/nc.openbsd`: openbsd 版本，强大很多。

都可以用 `apt-get install nc-traditional` 或者 `apt-get install nc-openbsd` 来选择安装。不管是 gnu 版本还是 openbsd 版本，都有新老的区别，主要是传送文件时 stdin 发生 EOF 了，老版本会自动断开，而新的 gnu/openbsd 还会一直连着，两年前 debian jessie 时统一升过级，导致网上的所有教程几乎同时失效。

下面主要以最新的 GNU 版本为主同时对照更强大的 openbsd 版本进行说明。

#### 端口测试

你在服务器 A主机（192.168.1.2） 上面 8080 端口启动了一个服务，有没有通用的方法检测服务的 TCP 端口是否启动成功？或者在 B 主机上能不能正常访问该端口？

进一步，如果而 A 主机上用 netstat -an 发现端口成功监听了，你在 B 主机上的客户端却无法访问，那么到底是服务错误还是网络无法到达呢？我们当然可以在 B 主机上用 telnet 探测一下：

```bash
telnet 192.168.1.2 8080
```

但 telnet 并不是专门做这事情的，还需要额外安装，所以我们在 B 主机上用 netcat：

```bash
nc -vz 192.168.1.2 8080
```

即可，v 的意思是显示多点信息（verbose），z 代表不发送数据。那么如果 B 主机连不上 A 主机的 8080 端口，此时你就该检查网络和安全设置了，如果连的上那么再去查服务日志去。

nc 命令后面的 8080 可以写成一个范围进行扫描：

```bash
nc -v -v -w3 -z 192.168.1.2 8080-8083
```

两次 -v 是让它报告更详细的内容，-w3 是设置扫描超时时间为 3 秒。

#### 传输测试

你在配置 iptable 或者安全组策略，禁止了所有端口，但是仅仅开放了 8080 端口，你想测试一下该设置成功与否怎么测试？安装个 nginx 改下端口，外面再用 chrome 访问下或者 telnet/curl 测试下？？还是 python -m 启动简单 http 服务 ？其实不用那么麻烦，在需要测试的 A 主机上：

```bash
nc -l -p 8080
```

这样就监听了 8080 端口，然后在 B 主机上连接过去：

```bash
nc 192.168.1.2 8080
```

两边就可以会话了，随便输入点什么按回车，另外一边应该会显示出来，注意，openbsd 版本 netcat 用了 `-l` 以后可以省略 `-p` 参数，写做：`nc -l 8080` ，但在 GNU netcat 下面无法运行，所以既然推荐写法是加上 `-p` 参数，两个版本都通用。

老版本的 nc 只要 CTRL+D 发送 EOF 就会断开，新版本一律要 CTRL+C 结束，不管是服务端还是客户端只要任意一边断开了，另一端也就结束了，但是 openbsd 版本的 nc 可以加一个 -k 参数让服务端持续工作。

那么你就可以先用 nc 监听 8080 端口，再远端检查可用，然后又再次随便监听个 8081 端口，远端检测不可用，说明你的安全策略配置成功了，完全不用安装任何累赘的服务。

（点击 Read more 展开）

<!--more-->

#### 测试 UDP 会话

两台主机 UDP 数据发送不过去，问题在哪呢？你得先确认一下两台主机之间 UDP 可以到达，这时候没有 nginx 给你用了，怎么测试呢？用 python 写个 udp 的 echo 服务？？运维不会认你写的工具的，即使连不通他也会认为你的程序有 bug，于是 netcat 又登场了，在 A 主机上：

```bash
nc -u -l -p 8080
```

监听 udp 的 8080 端口，然后 B 主机上连上去：

```bash
nc -u 192.168.1.2 8080
```

然后像前面测试 tcp 的方法进行检测，结束了 CTRL+C 退出，看看一边输入消息另外一边能否收到，收得到的话可能是你自己的服务原因，收不到的话把 nc 测试结果扔给运维/系统管理员，让他们赶快检查网关和防火墙配置，系统自带的工具测试的结果，既简单又权威。

#### 文件传输

你在一台 B 主机上想往 A 主机上发送一个文件怎么办？不能用 scp / szrz 的话？继续 python 写个 http 上传？装个 ftpd 服务？不用那么麻烦，在 A 主机上监听端口：

```bash
nc -l -p 8080 > image.jpg
```

然后再 B 主机上：

```bash
nc 192.168.1.2 8080 < image.jpg
```

netcat 嘛，就是用于通过网络把东西 cat 过去，注意，老版本 GNU / OpenBSD 的 netcat 再文件结束（标准输入碰到 EOF），发送文件一端就会关闭连接，而新版本不会，你需要再开个窗口到 A 主机上看看接收下来的文件尺寸和源文件比较一下判断传输是否结束。

当传输完成后，你再任意一端 CTRL+C 结束它。对于新版 OpenBSD 的 netcat 有一个 -N 参数，可以指明 stdin 碰到 EOF 就关闭连接（和老版本一致），我们写作：

```bash
/bin/nc.openbsd -N 192.168.1.2 8080 < image.jpg
```

你机器上的 nc 命令有可能指向 /bin/nc.traditional 或者 /bin/nc.openbsd 任意一个，这里显示指明调用 openbsd 版本的 netcat。

这样在 openbsd 新版本的 netcat 中使用 -N参数，就不需要再开个终端去手工检查传输是否完成，传输结束了就会自动退出。其实 GNU 版本的 netcat 也有可以加个 -q0 参数，达到和 openbsd 版本 -N 的效果：

```bash
/bin/nc.traditional -q0 192.168.1.2 8080 < image.jpg 
```

只不过是 Linux 下面最新的 GNU netcat，对应 Windows 版本 没有该参数，所以从 Windows 传文件过去时，少不了再开个终端看一下进度，如果是 Linux 端发送就没问题了。通过管道协作，搭配 tar 命令，还可以方便的传一整个目录过去，有兴趣可以自己研究。

使用 netcat 这个系统默认安装的工具进行文件传输，可以算作你保底的手段，当 scp/ftp 都没法使用的情况下，你的一个杀手锏。

#### 网速吞吐量测试

最简单的方法，GNU 版本的 netcat 加上 -v -v 参数后，结束时会统计接收和发送多少字节，那么此时 A 主机上显示运行 GNU 版本的 nc 监听端口：

```bash
/bin/nc.traditional -v -v -n -l -p 8080 > /dev/null
```

加 n 的意思是不要解析域名，避免解析域名浪费时间造成统计误差，然后 B 主机上：

```bash
time nc -n 192.168.1.2 8080 < /dev/zero
```

回车后执行十秒钟按 CTRL+C 结束，然后在 A 主机那里就可以看到接收了多少字节了，此时根据 time 的时间自己做一下除法即可得知，注意 GNU 的 netcat 统计的数值是 32 位 int，如果传输太多就回环溢出成负数了。

对于 OpenBSD 版本的 nc 我们可以用管道搭配 dd 命令进行统计，服务端运行：

```bash
nc -l -p 8080 > /dev/null
```

客户端运行 dd 搭配 nc：

```bash
dd if=/dev/zero bs=1MB count=100 | /bin/nc.openbsd -n -N 192.168.1.2 8080
```

结束以后会有结果出来，注意这里使用了 -N 代表 stdin 碰到 EOF 后就关闭连接，这里凡是写 nc 命令的地方，代表 GNU/OpenBSD 任意版本的 netcat 都可以，显示的指明路径，就代表必须使用特定版本的 netcat，上条命令等效的 GNU 版本是：

```bash
dd if=/dev/zero bs=1MB count=100 | /bin/nc.traditional -n -q0 192.168.1.2 8080
```

其实上面两种方法都把建立连接的握手时间以及 TCP 窗口慢启动的时间给计算进去了，不是特别精确，最精确的方式是搭配 pv 命令（监控统计管道数据的速度），在 A 主机运行：

```bash
nc -l -p 8080 | pv
```

然后再 B 主机运行：

```bash
nc 192.168.1.2 8080 < /dev/zero
```

此时 A 主机那端持续收到 B 主机发送过来的数据并通过管道投递给 pv 命令后，你就能看到实时的带宽统计了，pv 会输出一个实时状态：

```bash
 353MiB 0:00:15 [22.4MiB/s] [          <=>  ]
```

让你看到最新的带宽吞吐量，这是最准确的吞吐量测试方法，在不需要 iperf 的情况下，直接使用 nc 就能得到一个准确的数据。

### 系统后门

假设你用串口登录到 A 主机，上面十分原始，包管理系统都没有，sshd/telnetd 都跑不起来，这时候你想用 B 主机通过网络登录 A 主机有没有办法？

GNU 版本的 netcat 有一个 -e 参数，可以在连接建立的时候执行一个程序，并把它的标准输入输出重定向到网络连接上来，于是我们可以在 A 主机上 -e 一下 bash：

```bash
/bin/nc.traditional -l -p 8080 -e /bin/bash
```

按回车打开系统后门，然后再 B 主机那里照常：

```bash
nc 192.168.1.2 8080
```

你就可以在 B 主机上登录 A 主机的 shell 了，操作完成 CTRL+C 结束。

对于 openbsd 版本的 netcat，-e 命令被删除了，没关系，我们可以用管道来完成，和刚才一样，在 A 主机上：

```bash
mkfifo /tmp/f
cat /tmp/f | /bin/bash 2>&1 | /bin/nc.openbsd -l -p 8080 > /tmp/f
```

然后 B 主机和刚才一样：

```bash
nc 192.168.1.2 8080
```

即可访问，用完注意将 /tmp/f 这个 fifo 文件删除。



#### 结 束

netcat 就是可以在命令行直接的方式操作 tcp/udp 进行原始的：监听，连接，数据传输等工作。然后搭配管道，实现灵活多样的功能，或者进行各种网络测试。

其实上面几个例子，并不是说明 “netcat 可以干这些事情” 而是通过举例开一下脑洞，看看搭配管道的 netcat 究竟有多强。

还有很多其他用法，比如你可以用 netcat + shell script 写一个 http 服务器，使用 fifo 搭配两层 nc 可以实现 tcp 端口转发，搭配 openssl 命令行工具和 nc 加管道可以把 ssl 的套接字解码并映射成裸的 socket 端口供没有 ssl 功能的工具访问。。。。

当然你要说，这么多复杂的用法你记不住，大部分你都可以用专业软件来代替，那至少你可以先尝试使用 nc 来做 tcp/udp 端口测试，不要再用 telnet/chrome 来测试端口是否可用了，后者太过业余。其他功能可作为备份手段，在极端恶劣的环境下使用一下，也许能帮助到你很多；再你有心情的情况下可以研究下如何使用管道搭配其他工具进行一些高阶操作就行。


PS：

- 实在想用老版本的 nc，就是 stdin 碰到 EOF 会自动断开连接结束程序那个版本，可以用 busybox 自带那个 nc，只是功能少点而已（Windows 的 busybox 也有 nc）。
- Windows 下载地址：[netcat 1.11 for Win32/Win64](http://eternallybored.org/misc/netcat/)
- 可以把 ncat 给 alias 成 nc，完全兼容，这是 nmap 自带的一个更好的 netcat 分支，比 openbsd 版本还强，debian/ubuntu 下面安装了 ncat 后 nc 命令就会指向 ncat。

