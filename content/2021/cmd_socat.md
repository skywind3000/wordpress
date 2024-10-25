---
uuid: 2644
title: 新版瑞士军刀：socat
status: publish
categories: 网络编程
tags: 网络,命令行
slug: 
date: 2021-01-31 22:12
---
我在《[用好你的瑞士军刀：netcat](/blog/archives/2641)》中介绍过 nc 和它的几个实现（bsd, gnu, nmap），netcat 还有一个最重要的变种 socat （socket cat），值得花一篇完整的文章介绍一下，它不仅语义统一，功能灵活，除了完成 nc 能完成的所有任务外，还有很多实用的用法：

基本命令就是：

```bash
socat [参数]  <地址1>  <地址2>
```

使用 socat 需要提供两个地址，然后 socat 做的事情就是把这两个地址的数据流串起来，把第左边地址的输出数据传给右边，同时又把右边输出的数据传到左边。

最简单的地址就是一个减号“-”，代表标准输入输出，而在命令行输入：

```bash
socat - -              # 把标准输入和标准输出对接，输入什么显示什么
```

就会对接标准输入和标准输出，你键盘敲什么屏幕上就显示什么，类似无参数的 cat 命令。除了减号地址外，socat 还支持：`TCP`, `TCP-LISTEN`, `UDP`, `UDP-LISTEN`, `OPEN`, `EXEC`, `SOCKS`, `PROXY` 等多种地址，用于端口监听、链接，文件和进程读写，代理桥接等等。

因此使用 socat 其实就是学习各类地址的定义及搭配方法，我们继续以实用例子开始。

#### 网络测试

这个类似 nc 的连通性测试，两台主机到底网络能否联通：

```bash
socat - TCP-LISTEN:8080               # 终端1 上启动 server 监听 TCP
socat - TCP:localhost:8080            # 终端2 上启动 client 链接 TCP
```

在终端 1 上输入第一行命令作为服务端，并在终端 2 上输入第二行命令作为客户端去链接。

联通后在终端2上随便输入点什么，就能显示在终端1上，反之亦然，因为两条命令都是把标准输入输出和网络串起来，因此把两个地址交换一下也是等价的：

```bash
socat TCP-LISTEN:8080 -               # 终端1 上启动 server 监听 TCP
socat TCP:localhost:8080 -            # 终端2 上启动 client 链接 TCP
```

因为 socat 就是把左右两个地址的输入输出接在一起，因此颠倒左右两个地址影响不大，除非前面指明 `-u` 或者 `-U` 显示指明数据“从左到右”还是“从右到左”。

同 netcat 一样，如果客户端结束的话，服务端也会结束，但是 socat 还可以加额外参数：

```bash
socat - TCP-LISTEN:8080,fork,reuseaddr      # 终端1 上启动 server
socat - TCP:localhost:8080                  # 终端2 上启动 client
```

服务端在 `TCP-LISTEN` 地址后面加了 fork 的参数后，就能同时应答多个链接过来的客户端，每个客户端会 fork 一个进程出来进行通信，加上 reuseaddr 可以防止链接没断开玩无法监听的问题。

刚才也说了使用 socat 主要就是学习描述各种地址，那么想测试 UDP 的话修改一下就行：

```bash
socat - UDP-LISTEN:8080               # 终端1 上启动 server 监听 UDP
socat - UDP:localhost:8080            # 终端2 上启动 client 链接 UDP
```

即可进行测试。

#### 端口转发

在主机上监听一个 8080 端口，将 8080 端口所有流量转发给远程机器的 80 端口：

```bash
socat TCP-LISTEN:8080,fork,reuseaddr  TCP:192.168.1.3:80
```

那么连到这台机器上 8080 端口的所有链接，相当于链接了 192.168.1.3 这台机器的 80 端口，命令中交换左右两个地址一样是等价的。

（点击 Read more 展开）

<!--more-->

这里 socat 比 nc 强的地方就体现出来了，nc 做转发时只能转发 1 次，第一条链接 accept 并且关闭以后 nc 就退出了，无法接受新链接，因此 nc 只适合单次使用。而 socat 加上 fork 以后，每次 accept 一个链接都会 fork 出一份来不影响接收其他的新连接，这样 socat 就可以当一个端口转发服务，一直启动在那里。还可以用 supervisor 托管起来，开机自动启动。

还可以用这个功能暴露一些 127.0.0.1 的端口出来供外面访问，比起 nc 的临时救急使用一下的场景，socat 是可以当一个服务长期运行的。

#### 远程登录

地址除了 `TCP` 和 `TCP-LISTEN` 外，另外一个重要的地址类型就是 `EXEC` 可以执行程序并且把输入输出和另外一个地址串起来，比如服务端：

```bash
socat TCP-LISTEN:8080,fork,reuseaddr  EXEC:/usr/bin/bash    # 服务端提供 shell
socat - TCP:localhost:8080                                  # 客户端登录
```

完善一点可以加些参数：

```bash
socat TCP-LISTEN:8080,fork,reuseaddr  EXEC:/usr/bin/bash,pty,stderr   # 服务端
socat file:`tty`,raw,echo=0 TCP:localhost:8080                        # 客户端
```

这样可以把 bash 的标准错误重定向给标准输出，并且用终端模式运行。客户端可以像刚才那样登录，但是还可以更高级点，用 tty 的方式访问，这样基本就得到了一个全功能的交互式终端了，可以在里面运行 vim, emacs 之类的程序。

更高级一点，使用 root 运行：

```bash
socat TCP-LISTEN:23,reuseaddr,fork,crlf exec:/bin/login,pty,setsid,setpgid,stderr,ctty
```

相当于在 23 端口启动了一个 telnetd 的服务，可以用 telnet 客户端来链接。

#### 网页服务

首先编写一个脚本：web.sh

```bash
#! /bin/bash
echo -e -n "HTTP/1.0 200\r\n"
echo -e -n "Content-Type:text/html\r\n"
echo -e -n "\r\n"

echo "<html><body>"
echo "now is $(date)"
echo "</body></html>"
```

这里我们用 `SYSTEM` 地址类型代替原来的 `EXEC` 执行命令，因为可以后面写 shell 命令：

```bash
socat TCP-LISTEN:8080,fork,reuseaddr SYSTEM:"bash web.sh"
```

这时你就可以用浏览器访问：http://localhost:8080 的端口了：

![](http://skywind3000.github.io/images/blog/2021/socat.jpg)

相当于每次请求的时候，socat 都会 fork 一个进程出来然后执行后面的命令，启动上面的脚本程序，并且将脚本的标准输入输出重定向给网络链接。

相当于原始的 cgi 程序了，我们可以用 shell 直接完成一个 cgi 程序并由 socat 提供 cgi 服务，偶然需要暴露一些服务器信息的话，可以这样弄一下，返回的 html 里搞一个自动刷新，然后打开浏览器，实时监控服务器的情况。

#### 文件传输

临时需要传输下文件，无需 scp：

```bash
socat -u TCP-LISTEN:8080 open:record.log,create    # 服务端接收文件
socat -u open:record.log TCP:localhost:8080        # 客户端发送文件
```

这里用了 -u 参数，意思是数据从左边的地址单向传输到右边的地址，大写 -U 的话是从右边单向传输到左边。

#### 透明代理

第一句是用于 socks 代理的，第二句用于 HTTP 代理：

```bash
socat TCP-LISTEN:<本地端口>,reuseaddr,fork SOCKS:<代理服务器IP>:<远程地址>:<远程端口>,socksport=<代理服务器端口>
socat TCP-LISTEN:<本地端口>,reuseaddr,fork PROXY:<代理服务器IP>:<远程地址>:<远程端口>,proxyport=<代理服务器端口>
```

他们都可以把本地端口的请求转换成使用代理服务器访问的请求，比如：

```bash
socat TCP-LISTEN:1234,fork SOCKS4A:127.0.0.1:google.com:80,socksport=5678
```

那么链接本地的 1234 端口，相当于通过代理服务器 127.0.0.1:5678 去链接 google.com 的 80 端口了，这里用了 `SOCKS4A` ，后面 `A` 的意思是让代理服务器去解析域名。

#### 其他用途

还有很多高级用法，比如用 socat 一键开启 vpn 网络，使用 socat 将 ssl 流量转化为裸的 tcp 流量等等，可以参考官方文档。不难发现，上面几个用法都比原始的 nc 要强很多，但是 nc 更小巧一些，也更容易获得：不管是路由器上，还是 busybox 的内置命令中，还是 nmap 工具包，都有 nc 的存在。

所以很多时候条件限制可能你只有 netcat 可以使用，那么就用 netcat，其他时候看你哪个用的更熟练一些就用哪个。不管端口转发还是传文件，还是透明代理，每项其实都有专业的软件可以用，但 netcat/socat 用熟了以后，他们的灵活度非常大，能够搭配组合出千变万化的功能来，在你只是偶尔需要处理某件事情，又不想或者无法安装专用软件的情况下，完全可以使用这两个工具完成很多任务。

所以，socat / netcat 还有 tcpdump 一起，可以说是最值得掌握的三条网络命令。

