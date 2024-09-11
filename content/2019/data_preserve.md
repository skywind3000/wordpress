---
uuid: 2554
title: 如何长时间保存重要数据？
status: publish
categories: 随笔
tags: 随笔
date: 2019-05-09 15:24
slug: 
---
我大学毕业时把所有资料刻录成几张 dvd，才几年就发现读取不了了，而我老爸读大学时候的笔记本，几十年后仍保存完好。我前几年保存在移动硬盘里的照片，因为搬家时摔了一次，完全毁坏了，但是我家里小时候的相册却能几十年没有事情。

所以今天数据存储固然比过去更加方便，但是可靠性却大为降低。硬件坏了你还可以花钱再买，数据丢了，你就再也无力回天了。数据对我来讲是最宝贵的东西，无数血与泪的教训后，让我开始深入思考，怎么样才能让我的数据长期安全的保存几十年甚至终身？

##### 可以用光碟么？

光碟是最廉价最受欢迎的介质，他们本来设计寿命是 10-20 年的，而一般情况你不要指望你光盘上的东西五年后还能正常读出来。即便一些号称长期保存百年以上的光盘，寿命也会由于我们各种不当行为大大降低，比如，没法按要求的条件保存（放桌面上被阳光暴晒变形），不小心刮花光盘，在盘面上留下指纹或者手上的油脂，这些都会促进光盘表面化学成分变质，最终导致你的数据损坏。

##### 可以用机械硬盘么？

这两年 HDD/SSD 技术进步很快，成本越来越低。8T 的 HDD 差不多只 1000 元人名币的成本，1T 的 SSD 也从过去的好几千元降价到 600 多了。HDD/SSD 都能组成阵列，用虚拟逻辑卷的形式跨越物理大小的限制，为你提供超大规模的连续存储空间。

然而当你想要维护更大规模的盘阵时，你基础硬件设施的成本会大幅上升，4路阵列和8路16路的成本完全不一样。同时更新换代快，我过去保存的几块 IDE/SATA 接口的硬盘，今天我已经没有任何可用的设备来读取他们了。

遗憾的是，不管是 HDD 还是 SSD 他们都不能长期可靠的保存数据，每年有 1% 的概率由于磁场变化造成 HDD 数据损坏，这个损坏率会随着硬盘寿命逐年变大。而 SSD 的寿命比 HDD 更短，同时他们还会受到温度的影响，如果长期处在40度以上的工作温度，二者的寿命都会减半。

<!--more-->

##### 可以用 raid 么？

Raid 能再你一块硬盘损坏时照样帮你保证数据不丢失，这也是常用方案之一，但是 raid 就万无一失了么？并非如此，因为硬盘设计寿命相同，一起买来的同一个品牌的硬盘，经常要坏就几块一起坏，我就试过两块 raid1 在不到 24小时的时间里先后坏掉。

同时民用电源各种不稳定，烧电器的经历大家都有过吧？由于 raid 下面几块盘都是接在一起，如果碰到电源问题，一个击穿，就全部都坏掉了。

##### 可以用云存储么？

云存储是成本最高的选项，最便宜的百度云 1TB 的大小每年要 200元。然而把数据交给云服务商是风险最大的事情，百度会随意扫描你的照片，我同事曾经传了个身份证扫描件到百度盘上，然后马上删除了，结果第二天百度盘就给他推荐 “证件钱包”服务。我另外一个同事好几 T 的视频放在百度上，全部被替换成“净网公告”：

![](http://skywind3000.github.io/word/images/2019/preserve-1.jpg)

再者网龄稍微长点的人都有共识，网络服务是不可靠的，不管是过去的各种免费空间还是几年前的各种网盘，说关闭就关闭了，有的给你备份一下，有的连备份机会都没有，一纸通知，说关就关。你很可能一段时间没登陆网盘，没留意到通知，而再登陆时就发现数据没了。

所以网盘只适合保存一些，临时的，非关键数据，比如电影这些，看完一遍丢了也就丢了，而关键数据想要长期保存的话，网盘是风险最大的地方。

##### 可以用大容量 U 盘么？

U盘或者移动硬盘的出现让我们比过去方便很多，但一般 U 盘都是有擦写寿命的，寿命往往比 HDD/SSD 更短，同时容易携带也就意味着容易损坏，物理损坏，或者因为太小了，放在哪里就忘记了，“丢U盘”想必大家都试过。家里有小孩更是，我的几张 SD 卡，被我儿子当积木玩了两天，就再也读不出来了。

除去物理损坏外，各种使用不小心（比如频繁插拔，忘记安全弹出），也容易造成 U 盘/移动硬盘的损害。尽管你很小心的用你的u盘，结果拿给家人搞点啥，几下可能就用坏了。

##### 有无办法终身保护好自己的数据呢？

各种办法尝试了好多年以后，我开始思考，一些国家档案馆动辄保存上百年的资料，他们是如何做到的呢？再这些过程中，物理纸张可能老化，损坏，丢失，连墨迹也都可能淡化。他们的保存方法有什么值得借鉴的地方么？

![](http://skywind3000.github.io/word/images/2019/preserve-2.jpg)

然后我花了一个多星期的时间调研传统档案管理的各种：方法，制度，原则。研究完后受到了不少启发。。。。

想要长期保存数据，其实是一个成本问题，你愿意花多少钱和精力来做这件事情，决定预算以后，你不能依靠某一种单独的媒介来想着存进去就一劳永逸，而应该设计属于你自己的备份流程，靠流程来保证数据安全，比如下面几个点供你选择参考：

第一：明确可靠性等级，即数据分级，核心数据，重要数据，普通数据，可丢失数据。不同层次的数据对可靠性的要求是不一样的，对应的方法也不一样。

第二：格式转存，特别对于媒体数据，有损图片：JPG->BPG 基本能够清晰度不变但是尺寸变为原来 1/3，无损图片：PNG->FLIF，基本又能减少一半，如果你是 BMP/TGA 等老格式，直接转为 FLIF/BPG，马上让你空间缩小十倍。音视频数据也可以用更先进的编码器进行转存，这样你的空间占用至少能省一半出来。但是不要用一些太偏门的格式，避免几年后没有合适的程序读取。

第三：使用好一点的介质，都是 DVD-R，便宜的有 1-2 元一张，贵的有 80-100 元一张，区别就是质量，硬盘也分监控盘，企业盘还是消费盘。如果手头不是那么紧张，尽量使用质量好点的介质来保存你的数据。

第四：定期转存，不管放什么介质里，都需要定期检查，修复，活动介质可以靠一些自动脚本来转存，非活动介质需要手动进行。

第五：重要数据至少存三分，热数据（工作集），备份，备份的备份。

第六：备份方案根据数据重要度进行区分，哪些数据只需要 raid 备份，哪些数据除了raid外，还需要定时冷备到另外一块物理硬盘？哪些数据还需要定期刻录光碟？

第七：尽量地理上多地冗余，即便家里地震了也可以从异地恢复出来。

第八：尽量把文件直接放在文件系统上面，而不是再弄一个打包文件把一堆文件打了包再存，当介质发生故障时，打包文件很难恢复，而直接放在文件系统上的文件相对容易恢复一些。

。。。。

\--

补充：

关于磁带，主要个人玩家玩起来门槛有点高，同时磁带照样会受磁场变化影响损坏数据，而且磁带和磁盘一样容易“掉磁”，所以长期用磁带保存数据一般都要放在防磁柜里。门槛太高了，以前用了好几年磁盘，不管是 2.5寸 还是 3.5寸，三天两头就坏掉一张，让我对“磁”的东西真的没多大信心。

关于 DVD/BD ，有机/无机刻录盘，档案盘，千年盘（M-DISC）和硬盘的专业比较：

[硬盘和光盘的存储数据寿命哪个更长、更可靠?](https://www.zhihu.com/question/29443987/answer/288623390)

还有一篇超详细的介质比较，连任天堂卡带都拿出来分析了：

[Data storage lifespans: How long will media really last? - StorageCraft](https://blog.storagecraft.com/data-storage-lifespan/)

