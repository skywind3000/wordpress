---
uuid: 2706
title: 《原神》也在使用 KCP 加速游戏消息
status: publish
categories: 游戏开发, 网络编程
tags: KCP
slug: 
date: 2022-11-08 10:28
---

最近看到米哈游《原神》的客户端安装文件里附带了 KCP 的 LICENSE：

![](https://skywind3000.github.io/images/blog/2022/genshin.jpg)

于是找米哈游的同学求证了一下，果然他们在游戏里使用 KCP 来保证游戏消息可以以较低的延迟进行传输，这里还有一篇文章分析了原神使用 KCP 的具体细节：

![](https://skywind3000.github.io/images/blog/2022/genshi2.png)

文章见：https://forum.ragezone.com/f861/genshin-impact-private-server-1191004/index7.html

KCP 是我之前开源的一套低延迟可靠传输协议，能够有比 TCP/QUIC 更快的端到端传输效果，适合游戏、音视频以及各类延迟敏感的应用。

欢迎大家尝试：

- https://github.com/skywind3000/kcp

目前使用 KCP 的商用项目包括不限于：

- 原神：米哈游的《原神》使用 KCP 降低游戏消息的传输耗时，提升操作的体验。
- SpatialOS: 大型多人分布式游戏服务端引擎，BigWorld 的后继者，使用 KCP 加速数据传输。
- 西山居：使用 KCP 进行游戏数据加速。
- CC：网易 CC 使用 kcp 加速视频推流，有效提高流畅性
- BOBO：网易 BOBO 使用 kcp 加速主播推流
- UU：网易 UU 加速器使用 KCP/KCPTUN 经行远程传输加速。
- 阿里云：阿里云的视频传输加速服务 GRTN 使用 KCP 进行音视频数据传输优化。
- 云帆加速：使用 KCP 加速文件传输和视频推流，优化了台湾主播推流的流畅度。
- 明日帝国：Game K17 的 《明日帝国》，使用 KCP 加速游戏消息，让全球玩家流畅联网
- 仙灵大作战：4399 的 MOBA游戏，使用 KCP 优化游戏同步

KCP 成功的运行在多个用户规模上亿的项目上，为他们提供了更加灵敏和丝滑网络体验。


