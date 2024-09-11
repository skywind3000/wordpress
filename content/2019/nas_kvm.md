---
uuid: 2538
title: Nas 系统的虚拟化方案
status: publish
categories: 未分类
tags: 命令行
date: 2019-01-21 23:47
slug: 
---
对搞技术的人来说，Nas 是个理想的玩具，既然是程序员用的 Nas ，自然要专业一点，不能像小白一样买台威联通或者群晖往哪里一放就行，如果这样，就没有必要继续往下读了。

就像有人喜欢买成品车，有人喜欢自己改装车；有人喜欢傻瓜相机，有人喜欢机械相机。如果你喜欢 DIY，想让自己家里的硬件发挥更大用途，让自己的 nas 系统更专业些，那么请继续。

有人说，生命的意义在于奉献；还有人说，生命的意义在于付出；然而对于 Nas 玩家来说，生命的意义只有两个字 -- “折腾”。

有人问：“Nas 还能玩出一朵花来？”，答案是：“当然能”，折腾 Nas 第一步就是上虚拟化环境，有这个基础，后面才能更好的搞其他东西。所以今天我们先把 Nas 虚拟化这个纲领性的问题给说清楚说透彻。


#### Nas 系统为什么要虚拟化？

首先是让一台物理机可以安装多个不同的隔离的操作系统，Nas 很多都是魔改 Linux，一机多用的话，除了可以自由的安装其他主流 Linux 发行版外，你还能装台 Windows 来跑迅雷。

其次，而对于程序员，往往还需要另外一个干净的标准 Linux 发行版作为一个开发/折腾的环境，比如 Ubuntu / Debian / Centos 这些，虚拟化后，你可以自由的折腾你的发行版，通过虚拟机隔离后，你乱折腾自己的开发环境也不会把 Nas 弄挂，把自己的数据弄飞。

最后，资源分配更加灵活，系统/磁盘级别的备份迁移和恢复也可以很方便的实现。

<!--more-->

#### Nas 需要承担 HTPC 的角色么？

我说了一千遍了，HTPC 是一个伪需求，比如你家里有台电视还有一台投影仪，你是把 HTPC 接到哪里呢？还是配置两台 HTPC 各连一台，然后一个电影存两份？所以说这些方式都是扯淡的，Nas 就做好 “数据服务”这件事情就好了，就该安安静静的呆在路由器旁边，用网线直连，提供最好网速。

至于各种电视，投影仪，外接一个两百元的“盒子”或者 HDMI 电视棒即可，都可以通过无限播放局域网的视频。Nas 上各启动一些 Samba ，Plex ，Kodi，Emby 之类的，提供不错的检索分类服务，手机和 iPad 上也有各种 App 来直接串流。

所以 Nas 管好数据就行了，家里那么多块屏幕，采用局域网串流的形式比 HTPC 靠谱的多。


#### 方案 A：Nas 直接安装在物理机上，再在 Nas 里装虚拟机

这是最简单通俗的方法，优点是贴近硬件，Nas 直接面向硬件，能够提供更好的数据性能。你买一台成品威联通或者群晖来，他们都自带虚拟化环境，可以往里面安装各种虚拟系统。这是最简单直观的方案了。

那么该方案有什么不足么？当然有， Nas 安装到物理机上后，想在 Nas 系统上面继续安装一套完美的虚拟化环境，几乎是不可能的。Nas 系统定制化太深，你如果想在上面深度折腾虚拟机，会有很多限制。

再者 Nas 系统一般内核版本都是锁定版本的，我那台威联通，至今还是 Linux 4.2 的系统，跑个 KVM 虚拟化环境也用不到最新的内核，享受不了最新的虚拟化技术。

最后你没有办法自由的尝试各种 Nas 系统，比如你如果物理机上面安装一个 FreeNas ，它是 FreeBSD 系统，功能是强了，但是虚拟化就比较麻烦了，FreeBSD 下面没有啥好的虚拟化系统。因此，我们需要方案 B。

#### 方案 B：物理机直接变成 Hypervisor

这个方案是最干净的方案，先在物理机上把虚拟化系统搭建扎实，再在虚拟系统里安装你想尝试的各种 Nas 系统，即使 Nas 被你弄挂了，也可以用各种快照，恢复技术来拯救你的系统和数据，再者 Nas 系统里面各种权限设置，备份任务，各种服务和 App 搭建一次确实不容易，虚拟化以后，今后物理机升级也可以方便的迁移，同时硬件资源的分配也会更加灵活。

至于你在虚拟系统里安装什么 Nas，问题都不大，不管是基于 Linux 的黑群晖，开源的 OpenMediaVault，HP 合作的 ClearOS 还是基于 FreeBSD 的 FreeNas，你在虚拟机里面折腾都安全的多，不会把其他系统弄挂。

#### 使用何种虚拟化方案？

最简单的方式把一台物理机变成一台 Hypervisor 当然是安装 Windows，在上面弄个 HyperV，Vmware 再弄点随即启动什么的，或者弄点 vShpere。这样也可以，至少你没有用 VirtualBox 这些业余方案，但是 VmWare 系列限制也很多，非开源软件，免费版有 vCPU 数量限制，同时 VmWare 不支持类似 virtio 或者 vGPU 之类的事情。

更专业点的做法，当然是上 KVM 系统，该系统同 Vmware 之类的比较我不想多说了，就讲一点，今天不管阿里云，腾讯云还是境外 Linode / Aws 全部都跑在 KVM 为基础的系统上，它的应用规模比 VmWare/vShpere 广泛很多，能过够更好的同 Linux Guest OS 结合。

对于 KVM 系统，最弱智的玩法是 Ubuntu 桌面下面安装个 Virt Manager，然后像 VmWare 一样用，最专业的玩法当然是基于 OpenStack 和自己开发。对于个人用户，前者太过简陋，后者又太过复杂。所以对于个人用户我推荐 Proxmox VE，我在前文介绍过：

[KVM 虚拟化环境搭建 - ProxmoxVE](http://www.skywind.me/blog/archives/2527)

它基于 Debian，并使用了最新 Linux 内核和硬件驱动，直接刻录好碟/USB在裸物理机上安装就行了，然后通过 Web 界面来管理你的虚拟机。对于爱折腾的人，可以看：

[KVM 虚拟化环境搭建 - WebVirtMgr](http://www.skywind.me/blog/archives/2530)

在 Debian/Ubuntu 上采用开源方案，从零搭建一套类似 Proxmox VE 的系统。不管选择什么方案，花点时间将虚拟化系统摸清弄透，能够让你后面各种 Nas 的 Guest OS 稳定高效的运行。

#### 使用虚拟化系统不会损耗性能么？

KVM 系统对性能的损耗只有 1%-2%，这是官方数据，也符合我常年使用的经验。你看 AWS 上面用 KVM 跑着那么多高性能服务，有啥问题呢？

虚拟机都是基于 Intel VT-x 技术的，物理机 Hypervisor 其实运行在 vmx 的根模式下面，而虚拟机的每个 vCPU 则运行于非根模式中，每个 vCPU 通过一个独立的 VMCS 寄存器来描述，相当于沙盒环境，物理机通过一条 VMLAUNCH/VMRESUME 从根模式切换到虚拟机的非根模式，执行 vCPU 里面的指令，当需要发生 I/O 或者中断/异常时，又会退出回 Hypervisor 的根模式下。

所以各种 CPU 密集的运算，都是 vmx 的 vCPU 沙盒里跑的，相当于物理 CPU 执行正常指令只是环境变了一下而已，基本没啥损耗，这部分 KVM 的 vmx vCPU 调度是直接实现在内核里面的，性能做的不错。唯一就是 I/O 时需退出 vmx 跑回物理机处理，这是在所难免的事情，KVM 的好处是提供了 virtio，如果 GuestOS 支持 virtio（比如都是 linux 系统，或者 Windows 安装 virtio 驱动），这个操作可以绕过很多不必要的硬件模拟，在物理机上更高效直接的实现。

#### Raid / ZFS 跑在物理机上还是虚拟机里？

如果你是硬件 Raid，那么没得选，肯定是跑在物理机上面的，但是个人用户，一块入门 raid 卡基本要两千元，你是土豪当我没说。从成本角度考虑，软件 raid 现在已经很成熟了，威联通和群晖这些都是 linux 软件 raid ，一个 mdadm 程序做一些封装而已，一用用了好几年，也没见消费者反馈什么问题。

在物理机上直接跑 Raid/ZFS 最简单直接，虚拟机里的 Nas 系统需要硬盘了，就在物理机的 Raid/ZFS 分区里创建几个 qcow2 的磁盘映像文件，比如 200G 一个，创建好了扔给虚拟机系统就行，qcow2 扩容也方便。

如果你使用 Proxmox VE 系统，它直接支持 ZFS，你可以组建你的 zpool，然后在 Proxmox VE 的网页上就可以直接管理它，在上面新建虚拟机存储镜像。如果你用其他虚拟化方案的化，可以用 mdadm 或者自己安装 zfs。

对于个人使用，没必要所有存储设备都上 Raid，你有四块硬盘的话，可以用两块上 raid1 存重要数据，另外两块上 raid0 存非重要数据，物理机上最好弄一块单独的 ssd 装物理机操作系统，剩余空间还可以给虚拟机装操作系统，四块单独的硬盘就全部用来存储数据。

这个方案唯一问题就是一堆 qcow2 的文件，始终隔着一层，有些影响性能，同时不太好做一些关于 raid 的系统性实验，你要在物理机里折腾 raid，弄出问题来，下面一堆虚拟机都可能跪了。所以如果你想把 raid / zfs 从物理机隔离出来，放到虚拟机里直接接管，追求极致性能的话，你需要用到存储设备透传。

#### 虚拟系统里做 Raid 需要注意哪些问题 ？

如果选择虚拟机做 Raid 请注意缓存模式选择 writethrough 或者 none，不要用其他模式，这样可以保证虚拟机里面想写磁盘时，外面物理机会真的立马让它写盘，而不是物理机再缓存一次，物理机再缓存一次的风险就是，虚拟机里面的 zfs/mdraid 以为自己写到了磁盘里了，但是其实并没有，只是写到了物理机的缓存里，此时一掉电或者故障，数据就挂掉了。

除了虚拟机里在 qcow2 磁盘镜像上创建 Raid 外，性能更好的当然是用 KVM 的存储设备透传，将几块物理硬盘设备直接传递给虚拟机里面的 Nas 系统来管理，这样能获得最好的性能。在 libvirt 里，配置你的虚拟机 xml 文件，加入：

```xml
<disk type='block' device='disk'>
        <source dev='/dev/disk/by-id/ata-Corsair_CSSD-F120GB2_1109650632000461003B' />
        <target dev='hdc' bus='virtio' />
</disk>
```

即可把物理机的物理硬盘/物理分区，直接透传给虚拟机的 hdc 设备。如果你用 Proxmox VE 的话，可以参考下文，将一块西数 4T 的硬盘透传给虚拟机的 FreeNAS 系统：

[The Proxmox VE KVM-based All-in-One with FreeNAS](https://www.servethehome.com/the-proxmox-ve-kvm-based-all-in-one-freenas/)

就是直接网页上点点鼠标就完成设置了，十分方便。

#### 如何透传其他设备？PCI 透传有什么用？

上面说了存储设备透传，其实 Nas 系统中 USB 设备也是很重要的一个环节，你经常要插一块移动硬盘/U盘到 Nas 上，做点备份什么的。此时虚拟机中的 Nas 系统就需要用到 KVM 的 USB 透传同能了，操作起来和上面的存储设备一样简单：

现在物理机中查看 USB 设备：

```bash
$ /sbin/lsusb
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 005 Device 012: ID 0a5c:2110 Broadcom Corp. Bluetooth Controller
Bus 005 Device 003: ID 0483:2016 SGS Thomson Microelectronics Fingerprint Reader
Bus 005 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
Bus 004 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
Bus 003 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
Bus 002 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
```

然后配置 libvirt 的虚拟机 XML：

```xml
<domain type='kvm'>
  <name>windowsxp</name>
  …
  <devices>
    …
    <hostdev mode='subsystem' type='usb'>
      <source>
        <vendor id='0x0a5c'/>
        <product id='0x2110'/>
      </source>
    </hostdev>
  </devices>
</domain>
```

把设备号配置进去，比如你可以把你物理机前面板的两个 USB 口透传给你的 Nas 用，以后这两个口插入设备的话 Nas 就能响应。Proxmox VE 里面设置的话也类似，见它 wiki：

[USB Devices in Virtual Machines](https://pve.proxmox.com/wiki/USB_Devices_in_Virtual_Machines)

大部分时候透传存储设备和 USB 基本已经满足需求了，KVM 支持任意 PCI 设备透传给虚拟机，具体可以自行搜索 “KVM PCI passthrough"，可以彻底满足你的各种硬件需求。

除了透传 PCI 设备，KVM 还支持透传 GPU 给虚拟机，可以用来跑一些 GPU 加速的转码服务，或者在虚拟机里面跑一个 CUDA 显卡挖矿之类的程序，有兴趣可以搜索相关文档。

#### 物理机和虚拟机如何共享文件夹？

不管是 KVM 还是 VmWare，都支持将物理机上的某个文件夹共享给若干台虚拟机来访问，只不过 VmWare 的化，还需要在 GuestOS 里面安装 vmware 的驱动程序套件，用 KVM 的话，如果 GuestOS 是 Linux 的话，根本不需要额外的驱动程序。

物理机下面先配置下 XML：

```xml
    <filesystem type='mount' accessmode='mapped'>
      <source dir='/home/data/kvm/kfs'/>
      <target dir='kfs'/>
    </filesystem>
```

然后物理机准备一下共享目录：

```bash
sudo mkdir /home/data/kvm/kfs
sudo chown libvirt-qemu:libvirt-qemu /home/data/kvm/kfs
```

注意上面共享目录的权限需要和你虚拟机运行权限相同，qemu.conf 里有这个配置，你还可以在物理机 ps aux 看看虚拟机进程所属的用户和组。接下来虚拟机中编辑 /etc/modules 文件，添加下面几行：

```
loop
virtio
9p
9pnet
9pnet_virtio
```

虚拟机内加载内核模块：

```bash
sudo service kmod start
```

然后测试 mount：

```bash
sudo mkdir /mnt/kfs
sudo mount -t 9p -o trans=virtio kfs /mnt/kfs
```

这样，虚拟机中的 /mnt/kfs 就映射到了物理机的 /home/data/kvm/kfs 路径下。

测试成功的话，设置 /etc/fstab：

```
kfs             /mnt/kfs        9p      trans=virtio    0       0
```

修改完后，mount -a 测试，测试通过重启虚拟机即可。当然实在懒得折腾可以在物理机上启动一个 nfs 服务，然后虚拟机里面 mount 物理机的 nfs 文件夹，实测性能也不错。

#### 容器服务放在物理机上还是虚拟机上？

如今不少 Nas 服务都是以 Docker 的形式提供出来，我的建议是不管 Docker 还是 LXC ，都放到虚拟机里面去管理（虽然 Proxmox VE 支持在物理机上管理 LXC），如果 Nas 系统本身是 Linux 的话，可以直接放在 Nas 那台系统里面启动，这样可以直接跑在 Nas 的各种存储设备上。

有的 Nas 系统支持 web 管理页面上直接管理 Docker 容器，不支持的话，自己动手，现在 docker compose 已经很方便了，一堆 docker-compose 文件放在 github 上，要用的时候克隆下来，顺序 up -d 就启动好了，各种 Volume 也可以通过 Nas 的备份系统定时备份。



#### 结 尾

虚拟化其实是玩好 Nas 的第一步，好像从来没人提过这方面的话题，知乎上的 Nas 玩家都这么业余么？上面是几条我觉得需要注意的地方，既然程序员玩 Nas，咱们起步就得专业点。



\----

PS：为什么要这么折腾啊？

¯\(ツ)/¯

这只是刚刚开始。

