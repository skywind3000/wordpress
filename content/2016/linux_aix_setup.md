"=========== Meta ============
"StrID : 1924
"Title : Aix 折腾手记
"Slug  : 
"Cats  : 随笔
"Tags  : Linux
"=============================
"EditType   : post
"EditFormat : Markdown
"TextAttach : 
"========== Content ==========

早年开发工作主要在 FreeBSD进行，2006年后来切换到 Linux下，期间穿插使用了一下 Solaris，所以我的网络库一直都是只支持这三个系统。为了让网络库支持更多平台，网上购置了一台 IBM AIX 小型机，因为其他大部分非 Linux系统，今天基本都可以在虚拟机里面安装了，而 AIX系统，你真的没法虚拟。

弄了几天以后，发现真他妈的麻烦，强大是强大，但是真的太琐碎了，相比之下，Linux/FreeBSD之流基本是傻瓜了。不看说明直接操作 AIX的话，可能连开机都麻烦，或者关机没关对，下次直接启动不了。

文字终端就没什么好拍的了，先上一张图形桌面的靓照吧：

![](http://skywind3000.github.io/word/images/linux_aix_1.jpg)

是的你没看错，这就是 AIX 7，2012年的操作系统，就是那么的霸道，四处透着古典 Unix的味道。这样的机器今天还跑在各大银行的机房里，AIX系统管理员也拿着比 Linux系统管理员多几倍的工资，虽然工作岗位比较稀少。

下面来感受一下你想正常开关机，安装软件的话要怎么弄：

<!--more-->

查看微码：lsmcode 
光盘检测：开机键盘检测后按5光盘启动再按1
图形下设置网络： smitty tcpip

开机：
第一步：插电，风扇开始转，等两分钟
第二步：待前面板绿灯开始闪时，安白色开机键，绿灯长亮，等三分钟
第三步：显示器上出现画面，按提示进行操作

关机：
第一步：shutdown -F
第二步：等待系统结束后，显示器无信号，再等待一分钟
第三步：风扇降速，前面板绿灯从长亮回到闪烁状态
第四步：拔掉电源

解决亮黄灯：
第一步：root执行 diag
第二步：选择第2项，advanced diagnostics routines;
第三步：选择 system verification
第四步：选择 all resources
第五步：F7（或者 ESC+7）执行检测
第六步：看返回结果，是否存在故障，记录故障及errpt -a，再做处理


如果还不行补充1：
第一步：diag->task selection(diagnostics, advanced diagnostics, service aid）
第二步：identify and attention indicators
第三步：set system attention indicator to normal/set all identify …. To normal
第四步：F7执行
实在不行：# /usr/lpp/diagnostics/bin/usysfault -s normal

安装系统：
第一步：加电开机，插入安装 DVD
第二步：到系统键盘自检时按1，或者F1
第三步：输入密码（默认：admin）开始安装

更新微码：
危险：http://www-912.ibm.com/eserver/support/fixes 
查看处理器：prtconf

加载光驱：
mount -v cdrfs -o ro /dev/cd0/ /mnt

添加用户：
mkgroup dba
useradd -G dba -d /home/oracle -m oracle

全局变量：

```text
# cat /etc/environment 只能写 key=value
# cat /etc/profile 可以写shell脚本
```

分区操作：

```text
# lsvg rootvg 查看分区
# df -tk 查看文件系统按1K来查看
# chfs -a size=+2000000 /home 给home增加1G空间
```

安装软件：

```text
# smitty 安装系统包
# ftp ftp.software.ibm.com/aix/freeSoftware/aixtoolbox/RPMS/ppc 下载工具
# rpm -hUv xxx.rpm 安装工具
# rpm -e python 卸载工具
# rpm -qa 查看所有已经安装的包
# rpm -qpR xxx.rpm 查看依赖关系
# installp -qaXgd rpm.rte rpm.rte 安装 rte，或者试用smitty
# zcat xxx.tar.Z | tar -vxf -
```

第三方包：

```text
http://www.perzl.org/aix/index.php?n=Main.Apr-util
ftp://www.oss4aix.org/latest/aix71/
```

调试代码：

使用 truss 相当于 strace

。。。。。

玩了几天，看了N多 AIX资料，给程序增加了 AIX支持并调试正常后，觉得 IBM AIX System Administrator 认证（非 User）估计还真不是那么好考的。

