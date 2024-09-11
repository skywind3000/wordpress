The number of users of online games and social platforms is growing exponentially in recent years. The continued success of them hinges critically on the ability to deliver smooth and highly-interactive experiences to the end-users.

KCP is focusing on concurrent messaging, where messages are required to deliver to users wild at exactly the same time. I had been studying communication engineering at the university. Designing transmission protocol is one of my most favorite things. In the past I have designed five different protocols used in different areas and KCP is one of them which has been widely used in audio/video streaming, online gaming and other open source projects:


## Open Source Projects

### Kcptun 

![](http://skywind3000.github.io/word/images/kcp/kcptun.jpg)

[kcptun](https://github.com/xtaci/kcptun/blob/master/README.en.md) is a kcp+udp tunnel who uses KCP to speed up the transmission rate of traditional TCP applications. People far away from U.S. can use it with some proxy in their linode to watch 1080p videos from youtube, where they can only watch some 320p poor quality videos before by using TCP directly.

Kcptun is a popular:

![](http://skywind3000.github.io/word/images/kcp/kcptun2.jpg)

It has more than **1 million downloads** on github, and gets **3783 stars** now. It costs lower resource but gets higher performance than final-speed.

Last month, kcptun has been adopted by archlinux, see here:
[https://aur.archlinux.org/packages/kcptun-bin](https://aur.archlinux.org/packages/kcptun-bin)

Archlinux users are satisfied with it. Someone even port it to openwrt:
https://github.com/bettermanbao/openwrt-kcptun

### Lantern

![](http://skywind3000.github.io/word/images/kcp/lantern.jpg)

[Lantern](https://getlantern.org/) is a free application that delivers fast, reliable and secure access to the open Internet for users in censored regions. It uses a variety of techniques to stay unblocked, including domain fronting, p2p, and pluggable transports. https://getlantern.org.

It has integrated [kcp-go](https://github.com/xtaci/kcp-go) to reduce network latency and got **21770 stars** on github. 

### RPCX

![](http://skywind3000.github.io/word/images/kcp/rpcx.png)

[RPCX](https://github.com/smallnest/rpcx) is a distributed RPC service framework based on net/rpc like alibaba Dubbo and weibo Motan. One of best performance RPC frameworks.

### Many Others 

- [dog-tunnel](https://github.com/vzex/dog-tunnel): Network tunnel developed by GO, using KCP to greatly improve the transmission speed, and migrated a GO version of the KCP.
- [v2ray](https://www.v2ray.com)：Well-known proxy software, Shadowsocks replacement, integrated with kcp protocol after 1.17, using UDP transmission, no data packet features.
- [asio-kcp](https://github.com/libinzhangyuan/asio_kcp): Use the complete UDP network library of KCP, complete implementation of UDP-based link state management, session control and KCP protocol scheduling, etc.
- [kcp-java](https://github.com/hkspirt/kcp-java)：Implementation of Java version of KCP protocol.
- [kcp-go](https://github.com/xtaci/kcp-go): High-security GO language implementation of kcp, including simple implementation of UDP session management, as a base library for subsequent development.
- [kcp-csharp](https://github.com/limpo1989/kcp-csharp): The csharp migration of kcp, containing the session management, which can access the above kcp-go server.
- [kcp-rs](https://github.com/en/kcp-rs): The rust migration of KCP
- [lua-kcp](https://github.com/linxiaolong/lua-kcp): Lua extension of KCP, applicable for Lua server
- [node-kcp](https://github.com/leenjewel/node-kcp): KCP interface for node-js 
- [shadowsocks-android](https://github.com/shadowsocks/shadowsocks-android): Shadowsocks for android has integrated kcptun using kcp protocol to accelerate shadowsocks, with good results
- [libkcp](https://github.com/xtaci/libkcp): FEC enhanced KCP session library for iOS/Android in C++ (still in progress).
- [kcpuv](https://github.com/elisaday/kcpuv): The kcpuv library developed with libuv, currently still in the early alpha phase.


## Audio Streaming

### Fantastic Westward Journey II
![](http://skywind3000.github.io/word/images/kcp/xyq.jpg)

[Fantastic Westward Journey II](http://game.163.com/en/xyq.html) is developed and published by [NetEase](http://corp.netease.com). This game is originated from a Chinese classical novel, Journey to the West, and presented with Q-style characters to build a romantic game climate.

Fantastic Westward Journey II attracts more than 250 million registers, and sets more than 500 servers. The con-current user reached 2.71 million in 2012 and awarded as the most popular online game in China. 

I have implementated the in-game voice chat system for Fantastic Westward Journey II in early 2012, which allow gamers talk in realtime when they are busy in gaming. By taking the advantage of KCP, audio messages get lower round-trip-time and much smaller jitter than tcp. 


### Ghost Story

![](http://skywind3000.github.io/word/images/kcp/ghost-story.jpg)

After successfully using my in-game voice chat system in Fantastic Westward Journey II, 
[Ghost Story](http://news.mmosite.com/content/2016-10-06/a_chinese_ghost_story_fantasy_mmorpg_from_netease.shtml) (another MMORPG title by NetEase) adopt it to enable their players chat online in 2013.


### CC

![](http://skywind3000.github.io/word/images/kcp/cc-main.jpg)

[CC](http://cc.163.com/download) is a desktop IM application for gamers. You can create or join   **voice rooms** to chat with other gamers in the same room. It gets a similar audio quality as webrtc in most of time, but can do better when network gets busy in the evening.


## Video Streaming

### bobo.com

![](http://skywind3000.github.io/word/images/kcp/bobo.jpg)

[bobo.com](http://www.bobo.com) is an online entertainment live social platform. Previously anchor girls use RTMP to stream video data to the servers and get a poor quality, video always get stuck when tcp lag happens. Almost 30% audience get stuck every 5 minutes, **Stuck** means that video player switchs from **playing state** to **buffering state** because video packets can't always be delivered in time by using TCP with RTMP.

To improve their quality, I have implementated a KCP + Reed Solomon FEC transmission layer for them to replace the old TCP RTMP module in the anchor side. As a result, the number of users who get stuck drops from 30% to 8% every 5 minutes. 

### cc.163.com

![](http://skywind3000.github.io/word/images/kcp/cc-web.jpg)

[cc.163.com](http://cc.163.com) is a Twitch like game live streaming platform. The IM application of CC provides video streaming too, but you can watch the video directly on the  cc.163.com website without download the CC client.

## Games

Fast action games usually use a Lockstep or Dead Reckoning like strategy to synchronize game states between different players. All the strategies require a low latency transmission protocol and KCP has helped some of them to achieve more smooth user experience than libenet.

Many developer from different teams asked me how to tune KCP options to get better performance and their told me they had replaced tcp or libenet with KCP because they found KCP is far  better than them, but they don't like to tell me the name of their titles or their titles are  still in progress.

Here is the one I know:

![](http://skywind3000.github.io/word/images/kcp/game-1.jpg) ![](http://skywind3000.github.io/word/images/kcp/game-2.jpg)

["Smash of Gods" (仙灵大作战)](http://www.pc6.com/azyx/403918.html) is a MOBA mobile game which released in Dec. 2016.

