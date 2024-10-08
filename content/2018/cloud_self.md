---
uuid: 2549
title: 常用公有云的替换方案
status: publish
categories: 未分类
tags: Nas
date: 2018-11-20 14:58
slug: 
---
多年的教训换来一句话：“你的数据，你掌握”。归根结底，对于重要数据，最安全的做法不是把它交到别人手中，而是自己保管。

##### 文件云服务：百度盘，DropBox，iCloud，OneDrive

经历了 2015 年末国内网盘服务大面积关停以及百度网盘上面文件被管理员删除，iCloud 私密照片泄露的问题后，我意识到，重要文件应该自己管理，公有云服务做一个补充备份。

- OwnCloud：老牌开源文件服务，支持移动端，网页版，Win/Mac/Ubuntu 桌面版：

![](https://skywind3000.github.io/images/blog/2018/cloud-1.jpg)

- NextCloud：OwnCloud 核心团队出走后新做的项目，改了很多老bug，加了新特性：

![](https://skywind3000.github.io/images/blog/2018/cloud-2.jpg)

我更喜欢 NextCloud，文件同步很方便，放视频或者照片上去会帮你自动做成缩略图，再 Web 上方便查看，移动版也可以在线播放上面的音视频，而不必下载本地。

![](https://skywind3000.github.io/images/blog/2018/cloud-3.jpg)

上图是相册插件，集中管理网盘内所有图片，还有更多有意思的插件值得花时间好好探索。我做过个镜像，可以用下面的 Docker compose 配置文件一键安装：

<!--more-->

```yaml
nextcloud:
    image: skywind3000/nextcloud:default
    restart: always
    ports:
        - 8443:443
    volumes:
        - ./data:/var/www/nextcloud/data
        - ./config:/var/www/nextcloud/config
```

启动后，访问 https://localhost:8443 就可以进入管理员和数据库配置，个人使用 sqlite 足以，容器内还有一个 memcached 在 11211 端口监听，可以配置 NextCloud 加速。

还有 Linux 下面的命令行版本，可以命令行进行文件夹同步，比如我所有服务器上的 ~/.vim/cloud 文件夹就是和一个 nextcloud 云账户（小号）关联的，Vim 里配置一个快捷键就可以打开该目录下的文件进行编辑，一处更改，所有服务器都同时同步。

备份的话写一些脚本把 NextCloud 的某些数据定期备份到百度盘或者 OneDrive 上面。不过备份时要提醒大家注意的是，评论区里网友说的：

> 我也选择NAS，百度网盘每次登陆都要我创建智能证件包，简直不能更无耻。我都不知道它到底有没有读取我照片上的信息，因为我真的存了身份证照片在上面……估计是永远也删不掉了吧

看起来百度网盘会定期扫描你上传的所有照片，发现照片里有身份证信息，所以给这位网友推荐了“智能证件包”，我百度盘上从来只保存非重要信息，故从没见到这个推荐。

所以私有云的意义就在于你的东西不会天天被人翻阅或者扫描，所以即便备份到公有云，脚本里最好也打包加密一下。

##### 代码托管服务：Github

还记得 Google Code 关停的事情么？今天的 Github/Gitlab 也不是那么稳当，何况国内网络经常抽风，访问 Github/Gitlab 越来越慢，所以日常开发还是自己搭建代码托管服务更靠谱，速度更快，日常秒提交。

- GitLab （自架版本）：功能最强的开源代码托管系统，支持 ci：

![](https://skywind3000.github.io/images/blog/2018/cloud-4.jpg)

- GitBucket：轻量级的代码托管系统，仿照 BitBucket，比 GitLab 消耗更少资源：

![](https://skywind3000.github.io/images/blog/2018/cloud-5.jpg)

- Gogs：国人开发的代码托管系统，比 GitBucket 更加轻量级：

![](https://skywind3000.github.io/images/blog/2018/cloud-6.jpg)

GitLab 是 Ruby 写的，很费内存。个人和小团队使用推荐后两个，上规模了需要自动化部署和复杂的管理的话，可以用 GitLab。

前两个的搭建方式见：正确使用 Docker 搭建 GitLab/GitBucket 只要半分钟

##### 文档托管服务：Google Doc

代码放 git，但是重要文档推荐使用 SVN 来管理，放 git 上，一不小心还会被你一个 gc prune 所有的历史就没了。SVN 上一旦提交，永远删除不了，且本地的仓库尺寸会比较小一些，适合放一些个人的重要文件：

- 自己写过的文档，表格
- 签署过的合同扫描
- 各种证件扫描
- 部分特别珍贵的个人代码
- 对权限控制比较严格的东西

这些重要数据我是绝对不可能放到任何公有云上面的，使用基于 HTTPS 的 apache dav_svn 提供安全传输，写点小脚本进行周期备份。核心库基本上可以控制在 32G 以内，备份文件加密后，定期同步到网盘，nextcloud，远程vps 上面，一个 u 盘就可以拷贝走。

十分钟搭建 HTTPS 的 svn 服务：

https://github.com/skywind3000/docker/compose/https-svn-authz


##### 云笔记服务：EverNote, 有道云笔记，马克飞象

Evernote 离线笔记要付费，到现在都不支持 Markdown，插入代码也不支持色彩高亮；有道云笔记更新那么多版本，主要都在加广告和各种乱七八糟的社区。马克飞象只能免费使用10天，十天后就要收费了，而且过于小众，担心哪天停止服务。

开源云笔记有很多，最靠谱的一个莫过于 LeaNote：

![](https://skywind3000.github.io/images/blog/2018/cloud-7.jpg)

基本满足 Evernote 里面的各种需求，此外还有不少 Evernote 没有的功能：

- 插入代码支持语法高亮：这是 EverNote 里想要很久却没有的功能

![](https://skywind3000.github.io/images/blog/2018/cloud-8.jpg)

- 支持 Markdown：完整支持 Github 的各种语法格式

![](https://skywind3000.github.io/images/blog/2018/cloud-9.jpg)

- 篇笔记提供：只读模式（默认），编辑模式的切换，按 CTRL+E 切换

![](https://skywind3000.github.io/images/blog/2018/cloud-10.jpg)

这是个很贴心的功能，EverNote 里笔记编辑好后，经常需要阅读，特别手机版，有时候 EverNote 手机版里用手指滚屏，滚着滚着就变成编辑模式了。

LeaNote 所有笔记点过去默认都是只读模式，方便浏览，要修改了再 CTRL+E 进入编辑模式。这样你编辑 Markdown 的时候编辑模式是使用左右分屏，左右代码，右边预览的模式，编辑完了以后，在你查看笔记时，就是只读模式，显示 Markdown 代码的左边分屏就隐藏起来了，只保留文档预览部分方便你查看。

运行客户端后你可以选择登陆 LeaNote 官服，或者自建服：

![](https://skywind3000.github.io/images/blog/2018/cloud-11.jpg)

跟 EverNote / 有道云笔记一样，LeaNote 写了笔记可以发布成一个 URL ，共享给别人。不会有任何人员可以拿着你的笔记翻来翻去，更不会因为笔记误含关键字被删除或标记。此外 LeaNote 里还支持各种插件，这些可以花时间慢慢发掘。

##### 后记

上面是日常使用频率最高的几类公有云的替代方法，大家日常还在使用哪些好用的方案呢？欢迎发到评论区，另评论区的 

@李爽 做了一个云文件存储项目：

[eyebluecn/tank](https://github.com/eyebluecn/tank)

个人项目很难得，大家支持下。
