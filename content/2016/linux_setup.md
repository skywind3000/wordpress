"=========== Meta ============
"StrID : 1893
"Title : Linux 线上系统调优备忘
"Slug  : 
"Cats  : 随笔
"Tags  : Linux
"=============================
"EditType   : post
"EditFormat : Markdown
"TextAttach : 
"========== Content ==========
大公司呆久了，都会对 SA的依赖十分强烈，很多事情 SA都帮我们搞定了。如今控制成本，没有招聘 SA，又没有购买 VPS，从买物理机开始到 IDC部署，服务器调优，虚拟机管理，全部都是自己来，才发现，安装一台 Linux机器自己玩很简单，但是要达到线上服务器的标准，还有若干调优工作需要做，有 SA的日志是多幸福的事情啊。

**物理机设备驱动**

Dell服务器默认安装系统后会报找不到驱动:

```text
W: Possible missing firmware /lib/firmware/tigon/tg3_tso5.bin
```

因为 Debian/Ubuntu 的包都是开源的，默认开源驱动性能不行，于是需要添加 non-free源：

```text
deb http://ftp.de.debian.org/debian main contrib non-free
deb-src http://ftp.de.debian.org/debian main contrib non-free
```

然后：

```text
apt-get update
apt-get install firmware-linux-free firmware-linux-nonfree
```

解决 Dell驱动报错问题。


**配置限制**

查看 /etc/security/limits.conf 没有就新建，加入 core 和 nofile 的相关配置，比如：

```text
* soft nofile 65536
* hard nofile 65536
* soft core unlimited
* hard core unlimited
# End of file
```

之类的，不用到 `~/.bashrc` 里面调用 ulimit。


**网卡多队列**

打开内核网卡多队列支持，避免网卡中断都集中在 cpu0 上处理，多队列打开后，可以让网卡中断均摊到各个 cpu上，对提高并发十分有用：

```text
wget http://skywind3000.github.io/install/set_irq_affinity.sh
```

放到 `/etc/config` 目录下面（没有就新建），然后在 `/etc/rc.local` 里面加一行，每次重启就跑 `set_irq_affinity.sh` 且必须用 bash跑，参数传入需要开启多队列的网卡，以下是 `/etc/rc.local` 的内容：

```text
/bin/bash 
/etc/set_irq_affinity.sh eth0 eth1 eth2

exit 0
```

下面是 set_irq_affinity.sh 的代码：

<!--more-->

```text
# setting up irq affinity according to /proc/interrupts
# 2008-11-25 Robert Olsson
# 2009-02-19 updated by Jesse Brandeburg
#
# > Dave Miller:
# (To get consistent naming in /proc/interrups)
# I would suggest that people use something like:
#	char buf[IFNAMSIZ+6];
#
#	sprintf(buf, "%s-%s-%d",
#	        netdev->name,
#		(RX_INTERRUPT ? "rx" : "tx"),
#		queue->index);
#
#  Assuming a device with two RX and TX queues.
#  This script will assign: 
#
#	eth0-rx-0  CPU0
#	eth0-rx-1  CPU1
#	eth0-tx-0  CPU0
#	eth0-tx-1  CPU1
#

set_affinity()
{
    MASK=$((1<<$VEC))
    printf "%s mask=%X for /proc/irq/%d/smp_affinity\n" $DEV $MASK $IRQ
    printf "%X" $MASK > /proc/irq/$IRQ/smp_affinity
    #echo $DEV mask=$MASK for /proc/irq/$IRQ/smp_affinity
    #echo $MASK > /proc/irq/$IRQ/smp_affinity
}

if [ "$1" = "" ] ; then
	echo "Description:"
	echo "    This script attempts to bind each queue of a multi-queue NIC"
	echo "    to the same numbered core, ie tx0|rx0 --> cpu0, tx1|rx1 --> cpu1"
	echo "usage:"
	echo "    $0 eth0 [eth1 eth2 eth3]"
fi


# check for irqbalance running
IRQBALANCE_ON=`ps ax | grep -v grep | grep -q irqbalance; echo $?`
if [ "$IRQBALANCE_ON" == "0" ] ; then
	echo " WARNING: irqbalance is running and will"
	echo "          likely override this script's affinitization."
	echo "          Please stop the irqbalance service and/or execute"
	echo "          'killall irqbalance'"
fi

#
# Set up the desired devices.
#

for DEV in $*
do
  for DIR in rx tx TxRx
  do
     MAX=`grep $DEV-$DIR /proc/interrupts | wc -l`
     if [ "$MAX" == "0" ] ; then
       MAX=`egrep -i "$DEV:.*$DIR" /proc/interrupts | wc -l`
     fi
     if [ "$MAX" == "0" ] ; then
       echo no $DIR vectors found on $DEV
       continue
       #exit 1
     fi
     for VEC in `seq 0 1 $MAX`
     do
        IRQ=`cat /proc/interrupts | grep -i $DEV-$DIR-$VEC"$"  | cut  -d:  -f1 | sed "s/ //g"`
        if [ -n  "$IRQ" ]; then
          set_affinity
        else
           IRQ=`cat /proc/interrupts | egrep -i $DEV:v$VEC-$DIR"$"  | cut  -d:  -f1 | sed "s/ //g"`
           if [ -n  "$IRQ" ]; then
             set_affinity
           fi
        fi
     done
  done
done


# done
```

重启以后，cat 一下 /proc/interrupts里面，最右边网卡相关的中断是不是分摊到不同的cpu上面了。

**网络参数优化**

参考下面 /etc/sysctl.conf里面的优化选项和你 /etc/sysctl.conf 的具体内容，视情况更改：

```text
#
# /etc/sysctl.conf - Configuration file for setting system variables
fs.file-max = 100000

#表示开启SYN Cookies。当出现SYN等待队列溢出时，启用cookies来处理，可防范少量SYN攻击，默认为0， 
#是为了防止一定程度上的DOD的
net.ipv4.tcp_syncookies = 1

#表示开启重用。允许将TIME-WAIT sockets重新用于新的TCP连接，默认为0，表示关闭； 不是很建议设置，可能接受错误的数据
#net.ipv4.tcp_tw_reuse = 1

#表示尽量不启用交换分区。
vm.swappiness=0

#表示开启TCP连接中TIME-WAIT sockets的快速回收，默认为0，表示关闭。 
net.ipv4.tcp_tw_recycle = 1

#表示系统同时保持TIME_WAIT套接字的最大数量，如果超过这个数字，TIME_WAIT套接字将立刻被清除并打印警告信息。默认为180000，改为5000。
net.ipv4.tcp_max_tw_buckets = 10000

# 允许更多的PIDs (减少滚动翻转问题); may break some programs 32768
kernel.pid_max = 65535

#表示用于向外连接的端口范围。缺省情况下很小：32768到61000，改为1024到65000。 
net.ipv4.ip_local_port_range = 1024 65000

#记录的那些尚未收到客户端确认信息的连接请求的最大值。对于有128M内存的系统而言，缺省值是1024。 
net.ipv4.tcp_max_syn_backlog = 16384

#时间戳可以避免序列号的卷绕。一个1Gbps的链路肯定会遇到以前用过的序列号。时间戳能够让内核接受这种“异常”的数据包。这里需要将其关掉。
net.ipv4.tcp_timestamps = 0

#为了打开对端的连接，内核需要发送一个SYN并附带一个回应前面一个SYN的ACK。也就是所谓三次握手中的第二次握手。这个设置决定了内核放弃连接之前发送SYN+ACK包的数量。
net.ipv4.tcp_synack_retries = 2

#在内核放弃建立连接之前发送SYN包的数量。
net.ipv4.tcp_syn_retries = 2

#如果套接字由本端要求关闭，这个参数决定了它保持在FIN-WAIT-2状态的时间。对端可以出错并永远不关闭连接，甚至意外当机。缺省值是60秒。
#但要记住的是，即使你的机器是一个轻载的WEB服务器，也有因为大量的死套接字而内存溢出的风险，FIN- WAIT-2的危险性比FIN-WAIT-1要小，因为它最多只能吃掉1.5K内存，但是它们的生存期长些。
#表示如果套接字由本端要求关闭，这个参数决定了它保持在FIN-WAIT-2状态的时间。
net.ipv4.tcp_fin_timeout = 5

#当keepalive起用的时候，TCP发送keepalive消息的频度。缺省是2小时
net.ipv4.tcp_keepalive_time = 1200

#ip_conntrack如果超过限制会出现丢包错误，默认为65535
#net.ipv4.ip_conntrack_max = 655360

#ip_conntrack回收速度
#net.ipv4.netfilter.ip_conntrack_tcp_timeout_established = 180

#每个网络接口接收数据包的速率比内核处理这些包的速率快时，允许送到队列的数据包的最大数目。
net.core.netdev_max_backlog =  262144

#web应用中listen函数的backlog默认会给我们内核参数的net.core.somaxconn限制到128，而Nginx内核参数定义的NGX_LISTEN_BACKLOG默认为511，所以有必要调整这个值。
net.core.somaxconn = 262144

net.core.wmem_default = 8388608
net.core.rmem_default = 8388608
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216

net.ipv4.tcp_mem = 94500000 915000000 927000000

#系统中最多有多少个TCP套接字不被关联到任何一个用户文件句柄上。如果超过这个数字，孤儿连接将即刻被复位并打印出警告信息。这个限制仅仅是为了防止简单的DoS攻击
net.ipv4.tcp_max_orphans = 3276800

# 避免放大攻击
#net.ipv4.icmp_echo_ignore_broadcasts = 1

# 开启恶意icmp错误消息保护
#net.ipv4.icmp_ignore_bogus_error_responses = 1

# 开启并记录欺骗，源路由和重定向包
#net.ipv4.conf.all.log_martians = 1
#net.ipv4.conf.default.log_martians = 1

# 处理无源路由的包
#net.ipv4.conf.all.accept_source_route = 0
#net.ipv4.conf.default.accept_source_route = 0
# 开启反向路径过滤
#net.ipv4.conf.all.rp_filter = 1

#net.ipv4.conf.default.rp_filter = 1

# 确保无人能修改路由表
#net.ipv4.conf.all.accept_redirects = 0
#net.ipv4.conf.default.accept_redirects = 0
#net.ipv4.conf.all.secure_redirects = 0
#net.ipv4.conf.default.secure_redirects = 0

# 不充当路由器
#net.ipv4.ip_forward = 0
#net.ipv4.conf.all.send_redirects = 0
#net.ipv4.conf.default.send_redirects = 0

# Turn off the tcp_window_scaling 
# #net.ipv4.tcp_window_scaling = 0 
# # Turn off the tcp_sack 
# #net.ipv4.tcp_sack = 0 


#
```

参考上面的经验配置，按需要取消注释。


**修改时钟源**

查看当前时钟源和修改时钟源：

```text
# cat /sys/devices/system/clocksource/clocksource0/available_clocksource
# cat /sys/devices/system/clocksource/clocksource0/current_clocksource
# echo hpet > /sys/devices/system/clocksource/clocksource0/current_clocksource
```

之前发现有一台服务器同样进程耗费的 cpu比其他服务器高很多，经过查证开发同学在那个进程里频繁取系统时间，同时那台机器 gettimeofday之类的系统调用耗时比其他服务器要久。因为改代码已经来不及了，还好发现原来几台服务器的时钟源不同，经过修改后，取时间的系统调用时间大大下降。

**强制扫描磁盘**

机房突然停电，UPS没弄好，机器发生重启，一般会自动扫描硬盘，但是如果不放心要扫描主硬盘的话，可以手动来：

```text
touch /forcefsck
```

在根目录下面创建一个名为 `forcefsdk` 的文件即可，然后重新启动就会进入强制 fsck程序。