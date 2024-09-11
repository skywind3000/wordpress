---
uuid: 2527
title: KVM 虚拟化环境搭建 - ProxmoxVE
status: publish
categories: 未分类
tags: 命令行
date: 2018-11-11 13:36
slug: 
---
送大家一套完全开源免费的 VmWare / vSphere 的代替方案，代价是稍微动一下手，收获是你再也不需要任何商用付费的虚拟机软件了。KVM 整套解决方案一般分三层：

- KVM：内核级别的虚拟化功能，主要模拟指令执行和 I/O
- QEMU：提供用户操作界面，VNC/SPICE 等远程终端服务
- Libvirtd：虚拟化服务，运行在 Hypervisor 上提供 TCP 接口用于操作虚拟机的创建和启停

第一个是 Linux 内核自带，后两个是各大发行版自带的标准组件。这里的 qemu 不是原生的 Fabrice 的 qemu，而是定制的 kvm 版本的 qemu 。

你当然可以用 qemu-system-x86 程序写很长的一串参数来启动你的虚拟机，但是这样十分不友好，所以有了 Libvirtd 这个东西，将物理机的所有资源：存储/网络/CPU 管理起来，并且提供统一的服务接口。

那么 KVM + Libvirtd 有几种不同层次的玩法：

- 初级：在 /etc/libvirtd/qemu 下面用 xml 描述每一台虚拟机的配置，然后用 virsh 在命令行管理虚拟机，最后用 VNC/SPICE 按照配置好的端口链接过去，模拟终端操作。
- 中级：使用各种 libvirtd 的前端，比如基于桌面 GUI 的 Virt Manager 给你界面上直接编辑和管理虚拟机，桌面版本的 VNC/SPICE 会自动弹出来，像 VmWare 一样操作。
- 高级：使用基于 Web 的各种 virt manager 进行集群管理，比如轻量级的 WebVirtMgr / Kimchi，适合小白的 Proxmox VE。基本是用 WebVnc/Web
- 超级：上重量级的 OpenStack，搭配自己基于 libvirt （libvirtd 的客户端库，比如有 python-libvirt 的封装）写的各种自动化脚本。

前两种太弱智了，OpenStack 又基本需要一个 DevOps 团队才玩得转。所以作为个人或者中小团队，买了台硬件过来，想把它变成一套小型的阿里云，腾讯云的系统，可以在 web 上创建/配置虚拟机，装系统，管理硬件资源，进行迁移备份等，基本就是第三套解决方案。

不想折腾的话，最简单的做法是直接下载 ProxmoxVE 社区版的 ISO ，刻录到 U 盘里，按照安装普通操作系统一样的安装到物理机上，立马把你的物理机变成一台 Hypervisor：

![](http://skywind3000.github.io/word/images/2018/proxmox-1.jpg)

Proxmox VE 安装后启动，你可以登陆进去，ProxmoxVE 基于 Debian 9 ，进去可以用 apt-get 进行版本升级。接着按提示打开网页：https://your-ip:8006/ 用系统 root 密码登陆：

![](http://skywind3000.github.io/word/images/2018/proxmox-2.jpg)

ProxmoxVE 可以方便的管理各种硬件资源（计算，存储，网络）和虚拟机系统，你可以方便的新建一台虚拟机并进行硬件配置：

<!--more-->

![](http://skywind3000.github.io/word/images/2018/proxmox-3.jpg)

各项配置应有尽有：

![](http://skywind3000.github.io/word/images/2018/proxmox-4.jpg)

配置好了以后启动虚拟机，选择“console”就可以使用 webvnc 终端安装操作系统了：

![](http://skywind3000.github.io/word/images/2018/proxmox-5.jpg)

嫌终端太小看不过来的话，可点右上角的 Console 按钮，弹出一个终端独占窗口，全屏化安装：

![](http://skywind3000.github.io/word/images/2018/proxmox-6.jpg)

ProxmoxVE 除了上面这些功能外，还能方便的对虚拟机进行：复制，快照，迁移。你如果有硬盘阵列，它还能使用 ZFS 帮你做软件 Raid，保证数据安全性，不需要学习复杂的 zfs 命令行，web上点点点就出来了。

小到个人 Linux Box ，大到商用的虚拟化集群，Proxmox VE 都能帮你方便的管理起来，提供开箱即用的体验，全部都是基于开源免费方案。唯一的问题是 Proxmox VE 本身和 Sublime Text 一样属于付费软件，但是可以免费使用，只不过免费版每次登陆 web后台会弹出一个对话框：

![](http://skywind3000.github.io/word/images/2018/proxmox-7.jpg)

提醒你要去注册而已，不过连这个烦人的对话框也是可以干掉的，登陆到物理机的系统里面，修改一下 pvemanagerlib.js 这个文件的判断条件就行：

```bash
sed -i.bak "s/data.status !== 'Active'/false/g" /usr/share/pve-manager/js/pvemanagerlib.js
```

不过该对话框也只有登陆的时候才会出现一次，如果不是强迫症的话，犯不着更改。

个人使用的话，二十分钟就可以在安装完 Proxmox VE，里面创建三个虚拟机，一个跑黑群晖或者各种 Docker 容器，一个开发用 Ubuntu/Debian ，另外一个跑个 Windows 10，网络设置成桥接模式，同一个路由器下可以直接访问，最后把他们的电源选项都配置成随同物理机开机自动启动，妥了，基本满足日常使用。

跑 Windows 的话，web 上用 VNC 操作桌面效率太低了，可以考虑使用 SPICE ，或者安装完系统以后打开 Windows 的远程桌面服务，以后用远程桌面操作。

到这里，你真的不需要 VmWare / HyperV / vSphere 这些乱七八糟的东西了。性能问题？KVM对性能的损耗只有 1%-2% ，你就是 VmWare 再快，1%了不起了嘛？99% 和 98% 有区别么？当然 VmWare / HyperV 的图形性能模拟的不错，虚拟机里可以玩点小游戏，这属于娱乐需求了，跑后台服务的话基本不用考虑。
