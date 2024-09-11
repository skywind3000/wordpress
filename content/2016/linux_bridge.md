"=========== Meta ============
"StrID : 1909
"Title : Linux 网桥设置
"Slug  : 
"Cats  : 随笔
"Tags  : Linux
"=============================
"EditType   : post
"EditFormat : Markdown
"TextAttach : 
"========== Content ==========
在公司机房的物理机上架设 KVM虚拟化的时候，经常需要配置网桥，先要安装网桥工具：

```text
apt-get install bridge-utils   
apt-get install uml-utilities
```

编辑 /etc/network/interfaces，参考下面配置加入网桥配置信息：
 
```text
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet manual

auto br0
iface br0 inet static
	address 192.168.10.6
	netmask 255.255.255.0
	network 192.168.10.0
	broadcast 192.168.10.255
	dns-search dell1
	bridge_ports eth0
	bridge_stp off
	bridge_fd 0
	bridge_maxwait 0

auto eth1
iface eth1 inet manual

auto br1
iface br1 inet static
	address 14.152.50.6
	netmask 255.255.255.192
	network 14.152.50.0
	broadcast 14.152.50.63
	gateway 14.152.50.1
	bridge_ports eth1
	bridge_stp off
	bridge_fd 0
	bridge_maxwait 0
	# dns-* options are implemented by the resolvconf package, if installed
	dns-nameservers 114.114.114.114
	dns-search dell1

auto eth2
iface eth2 inet manual

auto br2
iface br2 inet static
	address 112.93.114.2
	netmask 255.255.255.224
	network 112.93.114.0
	broadcast 112.93.114.255
	gateway 112.93.114.1
	bridge_ports eth2
	bridge_stp off
	bridge_maxwait 0
	dns-nameservers 114.114.114.114
	dns-search dell1

```

上面配置针对双线接入多 IP的情况，这样 br0-br2就可以给虚拟机 guest使用了，br0是内网，br1-br2是电信或者联通出口。

