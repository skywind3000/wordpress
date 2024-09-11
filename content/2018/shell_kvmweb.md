---
uuid: 2530
title: KVM 虚拟化环境搭建 - WebVirtMgr
status: publish
categories: 未分类
tags: 命令行
date: 2018-12-28 13:45
slug: 
---
前文《[KVM 虚拟化环境搭建 - ProxmoxVE](https://www.skywind.me/blog/archives/2527)》已经给大家介绍了开箱即用的 PVE 系统，PVE 是方便，但还是有几点问题：

第一：始终是商用软件，虽然可以免费用，但未来版本还免费么？商用的法律风险呢？

第二：黑箱化的系统，虽然基于 Debian ，但是深度改造，想搞点别的也不敢乱动。

第三：过分自动化，不能让我操作底层 libvirt/qemu 的各项细节配置。

PVE 是傻瓜相机，智能又复杂，对小白很友好；WebVirtMgr 是机械相机，简单而灵活。多一个选择始终是好事，何况我们说完 PVE 之后还介绍 WebVirtMgr，那肯定是有它不可代替的优势的。

不管你是在中小公司研究 IT 解决方案，还是搭建自己的 HomeLab，虚拟化是一个绕不过去的砍，现在的服务都不会直接启动在物理机上，成熟的架构基本都是：

物理机-\>虚拟化-\>容器

这样的三层架构，也就是说虚拟化是一切服务的基础。通过下面的步骤，让你拥有一套完全开源免费的，属于你自己的，没有任何版权和法律问题的虚拟化环境。



#### 操作系统选择

发行版选择主要以 Debian/Ubuntu LTS Server 为主，二者我并无偏好，选择你趁手的即可。Debian 每两年一个大版本，Ubuntu LTS Server 也是每两年一个大版本。也就是说每年都有一个最新的，他们的支持周期都是五年以上，去年发布的 Debian 9 ，今年是 Ubuntu 18.04 LTS，明年又是 Debian 10。



#### 安装依赖

新安装操作系统以后，先安装必备的包：

```bash
sudo apt-get install libvirt-daemon-system libvirt-clients
sudo apt-get install sasl2-bin libsasl2-modules bridge-utils
```

将 /etc/default/libvirtd 里面的一行 libvirtd_opts 改为：

```
libvirtd_opts="-l"
```

<!--more-->

修改 /etc/libvirt/libvirtd.conf，保证下列配置生效：

```ini
# 允许tcp监听
listen_tcp = 1
listen_tls = 0

# 开放tcp端口
tcp_port = "16509"

# 监听地址修改为 0.0.0.0，或者 127.0.0.1
listen_addr = "0.0.0.0"

# 配置tcp通过sasl认证
auth_tcp = sasl
```


修改 /etc/libvirt/qemu.conf，取消 "# vnc_listen = ..." 前面的 # 注释（如有），变为：

```ini
vnc_listen = "0.0.0.0"
```

找到并把 user 和 group 两个选项，取消注释，改为 libvirt-qemu：

```ini
user = "libvirt-qemu"
group = "libvirt-qemu"
```

重启并查看服务的状态：

```bash
sudo service libvirtd restart
sudo service libvirtd status
```

到了这一步，依赖就准备好了。


#### 创建管理用户

ubuntu 18.04 LTS 需要修改一下：/etc/sasl2/libvirt.conf 文件，取消最后一行的注释，变为：

```
sasldb_path: /etc/libvirt/passwd.db
```

并保证 mech_list 的值为 digest-md5 ，ubuntu 18.04 中默认为 gssapi 不能用：

```
mech_list: digest-md5
```

客户端链接 libvirtd 需要用户名和密码，创建很简单：

sudo saslpasswd2 -a libvirt virtadmin
可以查看创建了哪些用户：

```bash
sudo sasldblistusers2 -f /etc/libvirt/passwd.db
```

继续重启服务：

```bash
sudo service libvirtd restart
```

测试用户权限：

```bash
virsh -c qemu+tcp://localhost/system list
```

使用 virsh 链接本地的 libvirtd 操作本地虚拟机，输入刚才的用户名和密码检查是否能够顺利执行，如果该命令成功则代表 libvirtd 的服务和权限工作正常。


#### 配置网桥

Debian 9 下面是更改 /etc/network/interfaces，注意设备名称 eth0 需要改为实际的名称：

```
# The loopback network interface
auto lo
iface lo inet loopback
# The primary network interface
auto eth0
iface eth0 inet manual
auto br0
iface br0 inet static
    address 192.168.0.2
    netmask 255.255.255.0
    network 192.168.0.0
    broadcast 192.168.0.255
    gateway 192.168.0.1
    dns-nameservers 192.168.0.1
    dns-search dell420
    bridge_ports eth0
    bridge_stp off
    bridge_fd 0
    bridge_maxwait 0
```

Ubuntu 18.04 中，使用 /etc/netplan 配置网桥，卸载 cloud-init，禁用 cloud-init 配置：

```bash
sudo apt-get remove cloud-init
sudo mv /etc/netplan/50-cloud-init.yaml /etc/netplan/50-cloud-init.disable
```

并且新建文件：/etc/netplan/10-libvirtd-bridge.yaml：

```yaml
network:
    ethernets:
        enp3s0f0:
            dhcp4: false
            dhcp6: false
    bridges:
        br0:
            addresses:
                - 192.168.1.8/24
            gateway4: 192.168.1.1
            nameservers:
                addresses: [ 192.168.1.1, 114.114.114.114 ]
                search: [ msnode ]
            interfaces:
                - enp3s0f0
    version: 2
```

注意上面的设备名称 enp3s0f0 以及 ip 网关等配置应按实际情况更改。

注意接口名字和 ip等，改为对应的内容，改完后：

```bash
sudo netplan apply
```

启用新的网络配置，然后重启网络看看网桥，是否正常：

```bash
sudo brctl show
```

并且查看网络是否正常。



#### 安装 WebVirtMgr

按照 WebVirtMgr 的官网首页的说明

安装依赖：

```bash
sudo apt-get install git python-pip python-libvirt python-libxml2 novnc supervisor nginx
```

克隆仓库：

```bash
cd /var/www
sudo git clone git://github.com/retspen/webvirtmgr.git
```

安装 Django 等 python 包：

```bash
cd webvirtmgr
sudo pip install -r requirements.txt
sudo ./manage.py syncdb
sudo ./manage.py collectstatic
```

按提示输入 root 用户密码，该用户后面将用来登陆 WebVirtMgr。

然后测试：

```bash
sudo ./manage.py runserver 0:8000
```

用浏览器打开 http://your-ip:8000 并用刚才的用户登陆看看行不行，成功的话，会看到：

![](https://skywind3000.github.io/images/blog/2018/virt-1.jpg)

然后点击右上角添加一个 connection，把 localhost 这个 libvirtd 的链接用 tcp 的方式添加进去，用户名和密码是刚才初始化的 libvirt 的管理员 admin 和密码：

![](https://skywind3000.github.io/images/blog/2018/virt-2.jpg)

链接如果能够正常添加的话，表明可以正常运行了：

![](https://skywind3000.github.io/images/blog/2018/virt-3.jpg)


然后 CTRL+C 退出。

#### 安装 Nginx

新建并编辑 /etc/nginx/sites-available/webvirtmgr 文件：

```nginx
server {
    listen 8080 default_server;
    server_name $hostname;
    location /static/ {
        root /var/www/webvirtmgr/webvirtmgr; # or /srv instead of /var
        expires max;
    }
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-for $proxy_add_x_forwarded_for;
        proxy_set_header Host $host:$server_port;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 600;
        proxy_read_timeout 600;
        proxy_send_timeout 600;
        client_max_body_size 1024M; # Set higher depending on your needs
    }
}
```

然后做一个该文件的软连接到 /etc/nginx/sites-enabled 下面，并删除默认软连接：

```bash
cd /etc/nginx/sites-enabled
sudo ln -s /etc/nginx/sites-available/webvirtmgr .
sudo rm default
```

然后重启服务

```bash
sudo service nginx restart
```

#### 完成安装

新建并编辑 /etc/supervisor/conf.d/webvirtmgr.conf：

```ini
[program:webvirtmgr]
command=/usr/bin/python /var/www/webvirtmgr/manage.py run_gunicorn -c /var/www/webvirtmgr/conf/gunicorn.conf.py
directory=/var/www/webvirtmgr
autostart=true
autorestart=true
stdout_logfile=/var/log/supervisor/webvirtmgr.log
redirect_stderr=true
user=www-data

[program:webvirtmgr-console]
command=/usr/bin/python /var/www/webvirtmgr/console/webvirtmgr-console
directory=/var/www/webvirtmgr
autostart=true
autorestart=true
stdout_logfile=/var/log/supervisor/webvirtmgr-console.log
redirect_stderr=true
user=www-data
```

把整个 webvirtmgr 的项目文件所有者改为 www-data：

```bash
sudo chown -R www-data:www-data /var/www/webvirtmgr
```

重启并查看结果：

```bash
sudo supervisorctl reload
sudo supervisorctl status
```

如果碰到错误，比如 Exited too quickly 那么到 /var/log/supervisor 下面查看日志。

完成后，浏览器打开：http://your-ip:8080/servers/

如果一切工作正常，那么恭喜你，WebVirtMgr 安装成功。



#### 开始使用

在 /home/data 下面创建 kvm 目录，用于放虚拟机磁盘镜像文件和 iso 文件

```bash
sudo mkdir -p /home/data/kvm
sudo mkdir -p /home/data/kvm/{images, iso}
sudo chown www-data:www-data /home/data/kvm/iso
```

你可以放在你喜欢的地方，/home 目录一般在 debian 下面会分配比较大的空间，所以把虚拟机相关的东西，放到 /home/data/kvm 下面。

然后浏览器登陆 webvirtmgr 的页面，选择刚才添加的 localhost 链接，webvirtmgr 可以同时管理多台机器的 libvirtd，这里我们以刚才添加的 localhost 链接为例。

首先到左侧的 “存储池”添加用于保存虚拟机映像的路径：

![](https://skywind3000.github.io/images/blog/2018/virt-4.jpg)

先点击 "New Storage" 添加一个类型为 “目录卷类型”的存储池，名字为 images，指向：

```
/home/data/kvm/images
```

继续点“New Storage”添加一个类型为 “ISO 镜像卷”的存储池，名字为 iso ，路径为：

```
/home/data/kvm/iso
```

你如果有多块硬盘，还可以继续添加一些其他位置用于保存虚拟机的磁盘镜像。

还差网络配置就妥了，点击左边 “网络池”：

![](https://skywind3000.github.io/images/blog/2018/virt-5.jpg)

原来只有一个 default 的 NAT 类型网络，那个 bridge 是我们需要点击 "New Network" 添加的桥接网络：

![](https://skywind3000.github.io/images/blog/2018/virt-6.jpg)

上面这个桥接名称，就是我们前面配置的网桥名称 br0。我们启动的虚拟机一般都会希望和物理机同处于一个内网下，拥有可以直接访问的 IP，因此基本都用桥接模式。

创建虚拟机

先创建磁盘映像，到左边的 “存储池”，然后选择 images 存储池：

![](https://skywind3000.github.io/images/blog/2018/virt-7.jpg)

点击最下面的添加镜像，添加一个 20G 的 qcow2，名字为 test1：

![](https://skywind3000.github.io/images/blog/2018/virt-8.jpg)

然后点击左边的 “虚机实例”，然后点击左上角的 “New Instance”：

![](https://skywind3000.github.io/images/blog/2018/virt-9.jpg)

不要使用它那些乱七八糟的模板，直接点击正上方的 “Custom Instance”，创建虚拟机：

![](https://skywind3000.github.io/images/blog/2018/virt-10.jpg)

在创建虚拟机的对话框里，点击“Add Image”添加刚才创建的 test1.img 镜像，然后再 "Add network" 添加类型为 bridge 的桥接网络，你如果想要所有虚拟机都处于一个虚拟内网的话，还可以再添加一块类型为 default 的网卡，就是默认的 NAT 类型。

完成后点 “创建”，咱们的虚拟机就有了：

![](https://skywind3000.github.io/images/blog/2018/virt-11.jpg)

这时候，可以到现前的 “存储池”的 iso 下面，上传两个操作系统的安装盘 iso 文件，然后回来这个 test1 虚拟机主页，选择设置，挂载 iso 文件：

![](https://skywind3000.github.io/images/blog/2018/virt-12.jpg)

选择我们刚才上传的操作系统 ISO 文件，并点击右边的“链接”按钮，然后可以到“Power”那里使用 “启动”按钮开机了，此时虚拟机出于“开机”状态：

![](https://skywind3000.github.io/images/blog/2018/virt-13.jpg)

然后选择 Access ：

![](https://skywind3000.github.io/images/blog/2018/virt-14.jpg)

点击 “控制台”，打开虚拟机的 webvnc 终端，开始安装操作系统：

![](https://skywind3000.github.io/images/blog/2018/virt-15.jpg)

网页版本的 Webvnc 图形性能一般，建议安装操作系统都用普通文本模式安装（可以选择的话），测试虚拟机可以正常启动以后，我们先把它强制结束了，进行一些必要设置。


#### 安全设置

如果的服务器暴露再公网上，一定要到 Access -> Console Password 下面设置个密码：

![](https://skywind3000.github.io/images/blog/2018/virt-16.jpg)

webvirtmgr 里点击控制台它会自动读取该密码，不需要你手工输入，但是这样就比没有密码安全很多了。

然后启动后，你可以到：设置->XML 那里查看一下 VNC 被分配的端口号和设置过的密码：

![](https://skywind3000.github.io/images/blog/2018/virt-17.jpg)

由于默认配置 VNC 都是使用 “自动端口”，这样更安全些，每次虚拟机启动，都会动态分配一个，再 XML 这里可以查看得到，这样你也可以不用 webvnc，而用自己的 VNC 客户端：

比如 Windows 下的 vnc-viewer，填入 ip 地址和端口号，然后点 "connect"：

![](https://skywind3000.github.io/images/blog/2018/virt-18.jpg)

提示输入密码，将上面 XML 里的密码复制粘贴过来即可：

![](https://skywind3000.github.io/images/blog/2018/virt-19.jpg)

然后点击 OK 开始显示终端屏幕：

![](https://skywind3000.github.io/images/blog/2018/virt-20.jpg)

#### 共享文件夹

这是个很基本的需求，想省事的话，nfs 共享一下也可以，但是 KVM 本身支持 Hypervisor 和虚拟机共享文件夹的，并且性能很好，可惜 PVE 里居然做不了，因为它不能改 XML。

再 “设置”-> XML 那里点击 “编辑”并在 <devices>... </devices> 中加入下面配置：

```xml
    <filesystem type='mount' accessmode='mapped'>
      <source dir='/home/data/kvm/kfs'/>
      <target dir='kfs'/>
    </filesystem>
```

accessmode 可以设置成：mapped，passthrough 或 none。物理机准备一下共享目录：

sudo mkdir /home/data/kvm/kfs
sudo chown libvirt-qemu:libvirt-qemu /home/data/kvm/kfs
所有虚拟机在物理机上都会以 libvirt-qemu 这个用户来跑（前面设置过 qemu.conf），所以需要保证你物理机上需要共享的路径的权限。同时 accessmode 建议设置成 mapped，这样会用文件信息里的 meta info 来保存虚拟机中的文件权限信息。

虚拟机中编辑 /etc/modules 文件，添加下面几行：

```
loop
virtio
9p
9pnet
9pnet_virtio
```

加载内核模块：

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

修改完后，mount -a 测试，测试通过重启虚拟机即可。



#### 后记

可能大家发现了 WebVirtMgr 本质就是一个轻量级的 web 管理后台，可以在一台机器上搭建 webvirtmgr 并管理内网所有的提供 libvirtd 服务的机器。

由于 webvirtmgr 项目本身简单清晰，不少成功项目的代码都是源自它的，比如 QNAP 产品线里的 “虚拟机工作站”，通过前面一番动手，相信你对 kvm/libvirtd/vnc 之类的运作机里已经很熟悉了。

该系统设计的比较好的一个点就是允许我编辑 XML，而前面提到的 PVE 居然不允许我在页面上修改 XML，KVM支持的功能非常丰富，很多都需要通过修改 XML 完成，比如常用的硬件透传，大家可以搜索 "kvm passthrough"：该功能可以把 pcie 总线上的设备传递给虚拟机，比如你的物理机上有两个 USB 插口，你可以将其中一个赋予虚拟机。或者把物理机的磁盘阵列全部传递给虚拟机，由虚拟机里面来组 raid，这样虚拟机里面装点黑群晖或者 clearos / openmediavault 之类的 nas 系统的话，可以方便的把磁盘阵列管理起来。

如果物理机有显卡的话，你甚至可以把物理机的 gpu 透传给虚拟机，这样虚拟机里面就可以跑需要 GPU 支持的任务了，比如挖矿之类，这些在 PVE 里都没法支持，这些都是 webvirtmgr 比 PVE 更灵活的地方。

更多的功能，留给大家慢慢探索吧。
