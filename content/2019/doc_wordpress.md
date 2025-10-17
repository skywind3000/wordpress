---
uuid: 2343
title: 用 Vim/VsCode 来写 WordPress 博客
status: publish
categories: 随笔
tags: Vim
slug: 
date: 2019-05-13 16:47
---

试用过一段时间各种静态页面博客系统，Hugo 这些，虽然发展的不错，但是比起 WordPress 来还是太弱了。WordPress 毕竟是发展了 15 年的东西各种功能和插件都比较完善。

所以这次回过头来重新使用 WordPress，顺便做了升级，速度更快了（升级 PHP7，引入页面缓存等），代码高亮等各种小功能也调优了一下，又加了一些类似热门文章和访问计数等小功能。

然后我写了一个命令行工具，可以让我在喜欢的文本编辑器里用 MarkDown 写博客，然后命令行发布到 WordPress，具体见 [markpress](https://github.com/skywind3000/markpress) 相关文档。

下面是一些调优后的效果，首先 Markdown 的代码块，使用 highlight.js 以后好看很多：

```cpp
#include <stdio.h>
int main(void)
{
    printf("Hello, World !!\n");
    return 0;
}
```

这个插件支持 185 种语言（包括 Vim）的高亮，可以选择 89 种主题，是目前最强的代码高亮解决方案。

MarkPress 页面生成基本尊崇 Github 规范：

1. 连接会被自动识别，只需要直写 URL，就会自动识别出来加上 `<a>` 标签。
2. 比如双波浪线包围的内容 `~~测试~~` 会被划掉显示为：~~测试~~。
3. 比如 Github Emoji，直接写 `:smile:` 的 shortcode，就会变成 :smile:

除此之外还有很多 github 没有的扩展，比如：

??? 折叠菜单点击左边箭头打开
    第一行隐藏的折叠内容
    第二行隐藏的折叠内容

MathJax 的内嵌公式，被 `$` 符号包围住的内容会被识别成 latex 公式：

    $z=\sqrt{x^2 + \sqrt{y^2}}$

得到：

$z=\sqrt{x^2 + \sqrt{y^2}}$

然后是 GraphViz 图形，现在在 MarkDown 中用 `viz-{引擎名称}` 开头的代码块：

`````
```viz-dot
digraph G {
   A -> B
   B -> C
   B -> D
}
```
`````

能被转换为内嵌 SVG 代码，并被主流浏览器正常显示：

<!--more-->

```viz-dot
digraph G {
   A -> B
   B -> C
   B -> D
}
```

再测试一下复杂图形，使用 circo 引擎：

`````
```viz-circo
digraph st2 {
 rankdir=TB;
 node [fontname = "Verdana", fontsize = 10, color="skyblue", shape="record"];
 edge [fontname = "Verdana", fontsize = 10, color="crimson", style="solid"];
 st_hash_type [label="{<head>st_hash_type|(*compare)|(*hash)}"];
 st_table_entry [label="{<head>st_table_entry|hash|key|record|<next>next}"];
 st_table [label="{st_table|<type>type|num_bins|num_entries|<bins>bins}"];
 st_table:bins -> st_table_entry:head;
 st_table:type -> st_hash_type:head;
 st_table_entry:next -> st_table_entry:head [style="dashed", color="forestgreen"];
}
```
`````

得到：

```viz-circo
digraph st2 {
 rankdir=TB;
  
 node [fontname = "Verdana", fontsize = 10, color="skyblue", shape="record"];
 edge [fontname = "Verdana", fontsize = 10, color="crimson", style="solid"];
  
 st_hash_type [label="{<head>st_hash_type|(*compare)|(*hash)}"];
 st_table_entry [label="{<head>st_table_entry|hash|key|record|<next>next}"];
 st_table [label="{st_table|<type>type|num_bins|num_entries|<bins>bins}"];
  
 st_table:bins -> st_table_entry:head;
 st_table:type -> st_hash_type:head;
 st_table_entry:next -> st_table_entry:head [style="dashed", color="forestgreen"];
}

```

MarkPress 使用了 python-markdown 当作 parser，有大量的各种扩展，可以慢慢探索。

有了这个命令行工具以后，我可以愉快的在 Vim / VsCode 里面书写 WordPress 博客了。

