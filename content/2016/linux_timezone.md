"=========== Meta ============
"StrID : 1904
"Title : Linux 硬件时区折腾备忘
"Slug  : 
"Cats  : 随笔
"Tags  : Linux
"=============================
"EditType   : post
"EditFormat : Markdown
"TextAttach : 
"========== Content ==========

前段时间折腾家中 Nas的虚拟化服务，有时候虚拟机系统时间总是快8个小时。Guest这边设好了，到了 物理机就会慢8个小时。网上说只要修改/etc/default/rcS中的 UTC=no就行了，但还是没反映，没办法，一步步找问题。发现在/etc/rcS.d/S05hwclock.sh有这样一段话：

```text
# 2012-02-16 Roger Leigh rleigh@debian.org
# - Use the UTC/LOCAL setting in /etc/adjtime rather than
# the UTC setting in /etc/default/rcS. Additionally
# source /etc/default/hwclock to permit configuration.
```
 
也就是说时间是按照/etc/adjtime设置的，而不是/etc/default/rcS，晕倒。查了下adjtime文件，原来这个才是现在调整时间的设置文件，那个rcS已经被忽略了，也就是网上的那些方法只适合以前的系统，看来走了不少弯路啊。

将 /etc/adjtime 第三行由 UTC 改为 LOCAL 即可。


