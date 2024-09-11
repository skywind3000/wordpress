"=========== Meta ============
"StrID : 1880
"Title : Linux 下配置 Iptables 端口转发
"Slug  : 
"Cats  : 随笔
"Tags  : Linux
"=============================
"EditType   : post
"EditFormat : Markdown
"TextAttach : vimpress_584832fd_mkd.txt
"========== Content ==========
经常需要对服务端的端口进行转发映射，让链接A服务器（202.181.55.93：8080）端口的所有tcp数据，forward到B服务器（106.185.43.22:80）端口，比如国内联通出国访问比较快，而电信比较坑爹，如果你家是电信网络，你却想畅快的访问境外的 vps，那么可以在你联通网络的境内服务器上进行这样一个端口映射，你链接境内服务器（201.181.55.93:8080）端口相当于链接境外服务器的（106.185.43.22:80）端口。

Linux内核的 Iptables很强大，它维护一组内核变量，使用 /sbin/iptables命令进行直接规则设置，且通过配置新规则，可以直接支持端口转发，简单在 A服务器上使用下面这个 shell脚本即可：

```text
#! /bin/sh

# create forward rule by source interface
# http://serverfault.com/questions/532569/how-to-do-port-forwarding-redirecting-on-debian
PortForward1() {
    local IN_IF=$1
    local IN_PORT=$2
    local OUT_IP=$3
    local OUT_PORT=$4
    local IPTBL="/sbin/iptables"
    echo "1" > /proc/sys/net/ipv4/ip_forward
    $IPTBL -A PREROUTING -t nat -i $IN_IF -p tcp --dport $IN_PORT -j DNAT --to-destination ${OUT_IP}:${OUT_PORT}
    $IPTBL -A FORWARD -p tcp -d $OUT_IP --dport $OUT_PORT -j ACCEPT
    $IPTBL -A POSTROUTING -t nat -j MASQUERADE
}

# create forward rule by source ip
# http://blog.csdn.net/zzhongcy/article/details/42738285
ForwardPort2() {
    local IN_IP=$1
    local IN_PORT=$2
    local OUT_IP=$3
    local OUT_PORT=$4
    local IPTBL="/sbin/iptables"
    echo "1" > /proc/sys/net/ipv4/ip_forward
    $IPTBL -t nat -A PREROUTING --dst $IN_IP -p tcp --dport $IN_PORT -j DNAT --to-destination ${OUT_IP}:${OUT_PORT}
    $IPTBL -t nat -A POSTROUTING --dst $OUT_IP -p tcp --dport $OUT_PORT -j SNAT --to-source $IN_IP
}

PortForward1 eth3 8080 106.185.43.22 80



# put this file on /etc/network/if-up.d
```

上面两个函数，一个是针对网卡，一个是针对本地IP设置转发，记得把这个脚本放到 `/etc/network/if-up.d` 下面并设置可执行权限（Debian/Ubuntu），每次开机重启时保证可以运行，即可。
