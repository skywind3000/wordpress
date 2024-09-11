---
uuid: 2648
title: 支持 Win10 的网络环境模拟（丢包，延迟，带宽）
status: publish
categories: 网络编程
tags: 网络
slug: 
date: 2020-04-13 23:15
---
升级 Windows 10 以后，原来各种网络模拟软件都挂掉了，目前能用的就是只有 [clumsy](http://jagt.github.io/clumsy/)：

![](http://skywind3000.github.io/images/blog/2020/clumsy_1.gif)

唯一问题是不支持模拟带宽，那么平时要模拟一些糟糕的网络情况的话，是不太方便的，而开虚拟机用 Linux tc 或者设置个远程 linux 网关又很蛋疼，于是我顺便给他加了个带宽模拟功能：

![](http://skywind3000.github.io/images/blog/2020/clumsy_2.jpg)

注意最下面的 "Bandwidth" 选项，打上勾的话，就能顺利限速了，注意上面的 Filtering 需要填写正确的 WinDivert 规则。

注意，统计包大小时用的是整个 IP 包的大小（包括各种协议头），所以你设置成 500 KB/s 的话，实际按 tcp 计算的下载速率会略小。

二进制下载：

- [clumsy-bandwidth-win32.zip](https://github.com/skywind3000/clumsy/releases/download/0.3rc3/clumsy-bandwidth-win32.zip)
- [clumsy-bandwidth-win64.zip](https://github.com/skywind3000/clumsy/releases/download/0.3rc3/clumsy-bandwidth-win64.zip)

想自己检查自己编译的话：

- https://github.com/skywind3000/clumsy


欢迎 PR。
