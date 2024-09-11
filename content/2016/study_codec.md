---
uuid: 2515
title: 学习视频编解码知识需要哪些前置知识？
status: publish
categories: 编程技术
tags: 视频
date: 2016-07-08 00:43
slug: 
---
如果要随便学学，便于日后使用那花两个星期买本书，配合网上文章就行了。

如果你想自己动手改 x264，为其添加一些你想要的东西，那么下面步骤你得耐心走完：

1: JPEG编码不但要学，还要自己实现，这是图像编码的基础，理解下yuv, dct, 量化，熵编码（不用参考 libjpeg，太庞大，建议参考 tinyjpeg.c，单文件）

2: MPEG2编码要学，现代编码器都是 block based 的，而 block based编码器的祖先就在MPEG2，理解下帧内编码，帧间预测，运动矢量，残差图等基础概念。具体代码可以看早期版本的 ffmpeg 的 avcodec，比如 mpeg12enc.c 代码也就1000多行，容易看，不过其中牵扯很多ffmpeg的内部数据结构，比如 picture, DCTELEM，各种 table，bitstream，vlc, swscale 等公共模块，缺点是文档少，优点是读了这些对你读其他 ffmpeg代码有帮助。

3: 自己实现一个类 MPEG2 编码器，最好自己从头实现个编码器，具体实现方式可以参考我的上面提到的 “视频编码技术简介”。

4: 参照 MPEG2的原理阅读 h.264的相关文章和书籍，了解和MPEG2的异同，比如先从intra入手，并且阅读 x264的早期版本代码，比如 2005年的版本，重点阅读 common 目录，基本的数据结构都在那里了，基本的图像，宏块，预测等都在那里了，阅读完以后阅读 encoder目录，了解程序的结构，2005版本的 x264是今天 x264的基础。

5: 阅读最新的 x264代码，并整理代码脉络，了解近年来引入的各种优化方法，然后 google, google, google .......

6: 愉快的修改 x264吧，比如增加搜索强度，修改预测范围，增加抗丢包特性，或者增加带内编码冗余，修改内部缓存策略，寻找降低编码延迟的方法，根据你的需求，修改，测试，修改，测试。。。。。。

7: 至于 MPEG4文件格式，可看可不看，一下午的事情。

参考阅读：

[视频编码器原理简介](https://www.skywind.me/blog/archives/1566)
