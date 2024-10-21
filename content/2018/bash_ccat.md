---
uuid: 3057
title: 自带语法高亮的 cat - ccat
status: publish
categories: 随笔
tags: 命令行,Linux
slug: 
date: 2018-11-13 16:32
---
cat 源代码时如果带上语法高亮，会不会让工作效率更高一些呢？我们来做一个吧：

```bash
function ccat() {
    local style="monokai"
    if [ $# -eq 0 ]; then
        pygmentize -P style=$style -P tabsize=4 -f terminal256 -g
    else
        for NAME in $@; do
            pygmentize -P style=$style -P tabsize=4 -f terminal256 -g "$NAME"
        done
    fi
}
```

把上面代码片段放入你的 .bashrc 中，并且安装依赖：

```bash
sudo pip install pygments
```

就可以跟 cat 一样的用法查看文件内容了：

![](https://skywind3000.github.io/images/blog/2018/bash/ccat1.png)

对比下老的 cat 效果：

![](https://skywind3000.github.io/images/blog/2018/bash/ccat2.png)

是不是清爽多了？

有人在网上推荐个类似的工具，Go 语言写的 [ccat](https://github.com/owenthereal/ccat)，效果丑死了：

![](https://skywind3000.github.io/images/blog/2018/bash/ccat3.png)

黑色背景下都看不清楚，这个一万多行的 Go 写的效果，比我们 10 行 bash 写的差远了啊。

--

补充：其他网友推荐的 sharkdp/bat 看了下效果也相当不错，但是你不想下载安装几兆的东西的话，上面十行代码就够了，熟练掌握 Bash，很多事情需要就自己撸，效果也还不错，自己动手丰衣足食，不用网上找，不用求人开发。





