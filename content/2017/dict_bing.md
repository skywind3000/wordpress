---
uuid: 2875
title: 《简明英汉必应版》震撼发布-全网收词量最多的离线词典，词频考纲标注（432万词条）
status: publish
categories: 未分类
tags: 神兵利器, 英语
slug: 
date: 2017-11-30
---
相信大家都有类似的体验，现在各种桌面在线词典在盈利的压力下，广告越来越多，查个单词都要提示你注册用户，加入社区，添加好友，关注新闻，学习每日一句，推荐英语课程，搞得启动越来越慢，干扰太多了，稍不留神点错了就万劫不复了。

我就想要简单直接的查词即可，可惜商业免费词典都不满足我的需求，后来把《XX词霸》，《X道词典》都卸载了，转投免费开源的 GoldenDict（可以安装各种离线词典），挂载《21世纪》搭配《朗文》《剑桥高阶》等学习词典，确实很好用，可惜这些大部头词典的收词量太少了，查10个词，有3个查不出来，又得点开网页，有道搜不到去金山，金山查不出来去必应，必应再查不出来就要点开谷歌翻译和 wiktionary 和 Urban Dictionary 等，有时候网络不好，点不开，有时候 vps 抽风谷歌翻译用不了。

这年头难道就没有办法让你随心所欲简单快捷的查个单词？于是我找到一个解决方案：**现在网上公开免费资源那么多，既然找不到现成的，自己做一个收词量超大的词典放到 GoldenDict / 手机欧陆 里不就完了？**

然后我制作了 340 万收词量的开源词典《[简明英汉增强版](https://github.com/skywind3000/ECDICT)》（支持 GoldenDict, 欧陆词典，BlueDict，mdict，edwin，Kindle 等），受到很多网友们的欢迎，半年不到，积累了五万多的下载量。其后再接再厉，补充更多短语、谚语、新词、俚语和专业术语，并对前20万基础词汇使用必应释义进行了校对，最终发布这个收录 432 万词条的《简明英汉必应版》。

网上有的它有，网上没有的它也有！！收词量 432 万是什么概念，参考下面：

- OALD8：7.2万词条
- 朗文5：6.2万词条
- Merriam-Webster's Collegiate Dictionary：11.9万
- 柯林斯 Cobuild 5：3.4万
- 21世纪：37.7万
- 有道本地增强版离线词库：40万
- 欧陆离线词库：40万

整合了市面上各类免费和开源资料，利用 BNC/COCA 语料库进行词频矫正，并使用 NodeBox, WordNet 等自然语言处理工具包对各类时态语态，派生词等进行补充和标注。再根据考试大纲和柯林斯星级还有牛津 3000 核心词进行标注，让你一眼就能看出这个单词的重要性。

（点击 more/continue 继续）

<!--more-->

#### 演示1：基本使用

![](https://skywind3000.github.io/images/blog/2017/dict/dict1.png)

看上面 GoldenDict放在最上面的《简明英汉必应版》，请忽略下面的剑桥高阶，上面单词，下面音标和解释，这些没有区别，关键标注有四处：

1) 音标后面：K 代表是牛津 3000 核心词汇，2 代表是柯林斯两星词。
2) 下面的衍生词：各类简明英汉词典都没有，我用 NodeBox + BNC 语料库分析生成的。
3) 考试大纲词汇标注，是否是四级词汇？考研词汇？
4) 大纲后面的词频标注：8139/8803 前面代表 COCA 词频（按 COCA 词频高低排序，第 8139 个单词），后面是 BNC 词频。

![](https://skywind3000.github.io/images/blog/2017/dict/dict2.png)

再来一张，perceive 不再牛津 3000 里，所以音标后没有 K，但是还有 2，因为他是柯林斯二星词汇。

![](https://skywind3000.github.io/images/blog/2017/dict/dict3.png)

同时根据 COCA, BNC 的词频前 20 万单词进行校对补漏，兼顾现代和传统，比如 Taliban （塔利班）这个词，这个词在各类 “简明英汉词典” 里和其他大辞典里都很难找到。BNC 前二十万词里没它，但是 COCA（美国当代预料库）里排名 6947，简直是重点高频词汇。可能大家都知道 牛津 3000，BNC 和 COCA，避免有人不知道，还是科普下：

Oxford 3000

> 牛津字典核心 3000 词汇 (The Oxford 3000 wordlist) 是由语言学家和有经验的教师根据语料库里的词频及释义重要程度，选出了最常用的 3000 个词汇作为 “定义词汇” 的。 李笑来老师说：“如果想用英英词典（哪怕是入门的 “学习词典”），那么就起码要先把这两三千个单词搞定之后再说。” 。

BNC：

> 英国国家语料库（British National Corpus，简称 BNC）是目前网络可直接使用的最大的语料库之一，也是目前世界上最具代表性的当代英语语料库之一。由英国牛津出版社﹑朗文出版公司﹑牛津大学计算机服务中心﹑兰卡斯特大学英语计算机中心以及大英图书馆等联合开发建立，于 1994 年完成。英国国家语料库词容量超过一亿，由 4124 篇代表广泛的现代英式英语文本构成。其中书面语占 90%，口语占 10%。

COCA：

> COCA “美国当代英语语料库”（Corpus of Contemporary American English）是这个世纪里最大的美国语言学研究项目，地位相当于影响深远的英国的 BNC-British National Corpus。我们目前使用的大多数英语词频表都是从BNC来的，换据话说都是英国英语的词频，而且是 1980 年代以前的词频。COCA 收集工作至今还没结束，目前收集了4亿词汇的文献资料。这 4 亿词汇的基础材料包括 1997-2017 二十年里阅读量最广泛的小说和杂志（“TIME”、“New Yorker”等都是项目的参与者），电影、电视节目，大量的电话记录和面对面谈话记录，甚至还包括 911 报告等...）。

**有了 COCA词频就好，为什么还要提供 BNC词频呢？**

很简单，BNC 词频统计的是近百年的各类资料，而当代语料库只统计了最近 20 年的。quay（码头）这个词在当代语料库里排两万以外，你可能觉得是个没必要掌握的冷词，而BNC里面却排在第 8907 名，基本算是一个高频词，为啥呢？可以想象过去乘船还是一个重要的交通工具，所以以往的各类文字资料对这个词提的比较多。所以你要看懂百年以前的各类名著，国外的什么帝王将相才子佳人，你会发现 BNC 的词频很管用；而新闻时政，COCA 很管用。所以只看一个，未免有失偏颇，两者都提供，有个对比。

![](https://skywind3000.github.io/images/blog/2017/dict/dict4.png)

同时制作了一个“免音标版” 删除了头部的词头及音标（柯林斯和牛津三千信息整合到最后一行），也许你 GoldenDict / 手机欧陆 里面已经有很多字典了，也许你不会象我一样把它在 GoldenDict 里面放第一个，那么你可以用这个“去音标版”，来避免词头音标占用太大空间，和其他词典一起放手机里看着舒服，保持小巧紧凑，其他都一样。

#### 演示2：选词

最早的《简明英汉词典》和《朗道词典》，都号称收词 40万左右，但里面光各种医学化学专用名词就超过20万，真正重要的词却经常搞漏，如中考高考到 GRE的一万五千核心词汇，他们居然能缺少两千左右。对比英国国家语料库（BNC）的词频数据，前十万高频词汇缺少一万二多；同时对比美国当代语料库前六万高频词汇，任然缺少一万多。

国内词库制作之不严谨，可见一斑，朗道字典（GoldenDict / StarDict 配套的那个），居然连 “learn” 这个单词都没收，搞笑吧？我不知道是 bug 还是什么。号称收词量最大的简明英汉词典，居然没有 “longtime”，当然他有词组 “long time”，但是近年来 longtime 已经链接为一个词了，并且词频很高。词频上升比较快的还有 Taliban ，这些他们都没收收录。喜闻乐见的《21世纪》，也有不少漏词，比如神奇的 through 和 dalit ，包括不限于国内某些著名的商业词典，很多号称收词量多，但是他们把词给收偏了，这就是人工选词和校对不可避免的问题，所以我们需要更科学的根据各类考试大纲和语料库对选词进行自动矫正。

到底该收录哪些单词呢？就基础词汇而言，选词程序先后分析了：

语料数据：考试大纲（四六级，托福雅思GRE等，必须覆盖到位），BNC语料库，美国当代语料库，华尔街日报（进20年语料数据库），经济学人12万词频表。

词典索引：Vocabulary.com，《牛津大辞典》，wiktionary.org，《朗文6》，《科林斯12》，《21世纪》，《台湾国家教育研究院双语词汇》，cdict-1.0-1.rpm（Linux 下开源英汉词典）。

#### 演示3：动词短语

阅读时就怕出现这种每个词都认识，但是连在一起都不认识的词组短语：

```text
kisses off
get away with
kiss and tell
round off
a sticky patch
double down on 
```

这些短语如果你查《牛津高阶》他们都是淹没在浩瀚无边的基本词汇里面，不信你可以查查OALD8里面的 get 这个词有多大的篇幅，要从这些庞大的释义里挑出一个小短语，是比较低效的。联网查的话，有道不一定有，你又跳金山，金山不一定有，你又跳 bing， bing 里再没有只有去 google 翻译，结果发现 google 给你乱翻译一通你就麻烦了，现在这些可以直接查了。

各大词典对短语词组收录其实做的并不好，不方便无法直接索引不说，收录还相当有限，《简明必应版》的词组短语，能为你节省不少时间。

短语选词参考过：《牛津短语动词词典》,《朗文动词短语》,《牛⑧成语动词短语》和《美国传统字典》，《短语词频词典》，《英语常用短语词典》。

#### 演示4：俚语收录

收录大量俚语，包括 Urban Dictionary 热门词汇，能找得到中文解释的都有中文解释，比如：Bromance（兄弟情），找不到中文解释的又是很热门的俚语，用英文解释代替，至少你在这里可以查得到什么意思，比如：

```text
Yoga Pants 
that make anyone look like they have an ass.
> "Damn when did Jillian get an ass".
> "She doesn't, its just the yoga pants".

dudevorce
When two male best freinds officially end thier friendship over a lame disagreement,
usually concerning a girl.
> Spencer and Brody got a dudevorce over Lauren.  
```

包括大家耳熟能详的：no zuo no die，you can you up 。还有不少国内任何一个在线词典都查不出来的词，比如：poorism 等，都能查得出来。

俚语选词参考过：《美剧基础词汇》，《Urban Dictionary》，《The Dictionary of Contemporary Slang 4th》，《ReNew McGraw-Hill’s Essential American Slang Dictionary》，《English Idims Sayings and Slang by Wayne Magnuson》，《Probert glossary of slang》。

#### 演示5：新词收录

继续检索《牛津大辞典》近17年来收录过的新词汇列表：

Previous updates | Oxford English Dictionary

对比增加欠缺词汇，很多 《牛津大辞典》收录的现代流行词汇，比如：

```text
Brexit（英国脱欧）
polytenize（聚拢）
hackathon（黑客马拉松）
hackdom（黑客圈）
discman（随身听）
veg（蔬菜，vegetable 在英国已经被逐渐简称为 veg了，牛津大词典于2008年收录该词）
```

都可以查得到了，我试着在有道上随便查了一个词：Brexit 结果提示：

```text
您要找的是不是:
breit
breast n. 乳房，胸部；胸怀；心情 | vt. 以胸对... 
```

矫正工作（比较单词表，补充欠缺的单词）经历了：

1) 各大词典的索引矫正：《OED》，《美国传统》等
1) 词频矫正：BNC 数据前 20 万数据，COCA 词频前 40 万数据
1) 考试大纲矫正
1) 口语流行词矫正
1) 书面语流行词矫正

基本上你想得到的词汇它有，你想不到的它也有。

#### 演示6：专业词汇

从天文到地理，植物到动物，自然到历史，文学到法律，经融到计算机，数学到化学，体育到军事，举几个例子：

```text
经融：real estate company （不动产公司），carrying charge （流动费用）
计算机：Gvim （文本编辑器 ）
历史：Confucianism（孔子思想），Curtin John（柯廷(1885～1945)，澳大利亚政治家、总理）
军事：covering force area（军事掩护区）
。。。。
```

这些词汇很多国内网络词典都查不到，也许你一辈子也都碰不上，但是碰上了能为你省不少时间。专业词汇选词先后扫描过：

百科类：《大英百科全书》，《McGraw-Hill Dictionary of Scientific and Technical Terms》，

历史类：《Oxford Dictionary of World History》，《圣经词典》

军事类：《美国国防部军语及相关术语词典2008》.

法律类：《牛津法律词典》，《The Lectric Law Library》，《英汉法侓用语词典》，《英汉法律词典》，《英汉法律缩略语词典》

经融类：《彭博社专业财经词汇》，《英漢雙解路透金融詞典》，《英汉财经词汇手册》，《英汉汉英经贸大辞典》，

投资等：《Investopedia》，《英汉证券期货和金融术语》，《现代英汉汉英商务词典》

会计类：《注册会计师（CPA)专业英语词汇大全》，《英汉汉英会计金融词典》

科学类：《英汉数学大辞典》，《英汉汉英物理学词典》，《英汉地理大词典》，《世界地名翻译大辞典》，《英汉生物学大词典》，《英汉天文学词典》

计算机：《Microsoft Computer Dictionary》，《WeboPedia》，《NetLingo》，《What Is Tech Target》，《Computer Desktop Encyclopedia》，《Computer Hope》

机电类：《Glossary of Electrical Terms》，《英汉汉英电子工程词典》，《英汉机械大詞典》，《英漢漢英機械設計詞》

文学类：《Babylon English Idioms and proverbs Glossary (Phrasal Verb Dictionary)》，《The Jargon Lexicon》

医学类：《全医08总动员》，《人体生理学词汇》，《英汉医学辞典》

其他类：《Merriam-Webster's Elementary Dictionary 2016》，《英汉食品词典》，《12万字的专业英语词典》，《体育项目名词》，《英汉汽车词典》

以及其他更多：海洋，地质，化学，石油，植物，动物等专业词典词汇。

#### 演示7：成语谚语

也许你的阅读材料里碰到喜欢堆彻词藻的作者：

```text
when the cat is away, the mice will play 
山中无老虎，猴子称霸王；猫不在的时候老鼠就会尽情玩耍

If you can't stand the heat stay out of the kitchen.
怕死，就别上战场；不耐热就别呆在厨房

honey catches more flies than vinegar
投其所好；蜜蜂比醋抓的苍蝇更多；献蜜罐子总比送醋坛子管用 
```

《简明英汉必应版》能帮你迅速了解这些谚语的含义，很多包括各种网络词典都查不到，本词典三个月的制作过程中，前后都有网友给我提供各种数据和索引，希望我补充进去，上面只是展示了一小部分而已。

#### 演示8：其他有意思的东西

比如地名， 收录的所谓地名，《简明必应版》收录的地名，不是伦敦纽约这些早已收录的大城市名字，不是 Bari（意大利东部港口）这些各个各家稍微有点名气的二线城市，这些词早就收录了。这次收录的地名是指你把谷歌地图拉到意大利，将意大利东南部一角（不是整个意大利），放大到整个屏幕，才能看到的地放，比如：

```text
Alberobello 
[地名] 阿尔贝罗贝洛 ( 意 )
Cisternino
[地名] 奇斯泰尼诺 ( 意 )
matera
[地名] [意大利] 马泰拉
```

这些各个的三线小城市之类的地名，10万词条，世界上差不多 200 个国家，平均一个国家至少有 500 个地名，所有该类词条前面增加 [地名] 二字，后面增加属于哪里，方便你区别，虽然缺少各地更多简介，但这里不是 wikipedia，至少让你知道这是个地名，大概方位在哪里。 同时平均一个国家 500 个地名对我们中国来讲还是少了点，专门针对大陆和港台，收录了更为详细的地名数据，比如：Hualian City （花蓮市，台湾地名） ，Zhanjiang （广东省湛江市），Tsim Sha Tsui （尖沙咀）。经常读到个香港英文地址蒙圈了吧？终于可以查中文对应了。。。。。。

#### 演示9：词形变换

大部分词典只有单词的 Lemma （不知道怎么翻译，词干？原型？），比如 gave 的 lemma 是 give，并不包含词形变换，所以你查一个动词的过去式也许查不到，需要词典软件有构词法支持（morphology），但是并不是所有词典软件都像 GoldenDict 一样支持构词法，比如欧陆就不支持，Kindle 也没有。

《简明英汉必应版》不需要构词法支持，就核心 40万词汇而言，包括所有单词的形变：

- 名词不论单数形式和复数形式都能查到并且有标注
- 动词不论什么时态都能查到并且有标注
- 形容词不论比较级还是最高级都能查到并且有标注

不当查得到这些衍生词，各个衍生词还做了标注，即告诉你它的原型词（Lemma）是哪一个，比如你查询 attics：

![](https://skywind3000.github.io/images/blog/2017/dict/dict5.png)

大部分离线词典一查 attics 之类的衍生词基本就跪了，这里不但查得出来，还有完整标注，极大的提高了阅读查词的体验，而构词法的数据库一般只有17万（Hunspell），这里是 40 万的基础词条。

#### 移动设备支持（Kindle / 欧陆）

平时习惯在移动设备上阅读的朋友们不用担心，传统 Kindle 字典单个词释义篇幅又太大，需要滚屏半天才看得出个所以然，Kindle 上滚屏体验很不好，效率低；而且传统 Kindle 词典收词量少的可怜，因此制作了一个 Kindle 的《简明英汉必应版》：

![](https://skywind3000.github.io/images/blog/2017/dict/dict6.png)

Kindle 版本收词没有其他版本那么多，因为 mobigen 太费内存，亚马逊又没有发布 64位版本，词条一多就崩溃掉了，因此 Kindle 版本选取了最重要的前 160 万词条，已然是 Kindle 上最大的词典了。

同时《简明必应版》包括词形变换和原型标注，你捧着移动设备阅读小说，碰到的动词基本上是过去式，碰到的名词大部分是复数，那些大部头的英语词典基本只有词干 Lemma，没有衍生词，使用各种大部头的英语词典直接抓词的话，经常查不到，十分低效，而用本词典，不管是动词，名词还是形容词的各种形态，你全都能查出来，整个阅读过程流畅不少。

同时发布欧陆词典 eudic 格式的《简明英汉必应版》，比官方标配词库强大10倍，而且手机不联网也能随便查这个相当于网络词典级别收词量的离线词典了，欧陆对大型 mdx 支持不好，经常查不到词，所以欧陆用户请使用 eudic 格式的专版。

#### CSS 美化版

发布《简明英汉必应版》第一版后，两个月不到，积累了两万多的用户，大家纷纷指出了其中存在的不少错误和不完善的地方，于是我陆陆续续修正了几十个问题后发布了最终版。期间主要还是在关注词条质量和数量，对排版花的时间较少，有网友帮我做了一个支持 css 的 mdx版本，并且调整了版面布局，美观了不少：

![](https://skywind3000.github.io/images/blog/2017/dict/dict7.png)

ornate：

![](https://skywind3000.github.io/images/blog/2017/dict/dict8.png)

Yoga Pants:

![](https://skywind3000.github.io/images/blog/2017/dict/dict9.png)

原型标注用其他颜色显示：

![](https://skywind3000.github.io/images/blog/2017/dict/dict10.png)

CSS 美化版使用分离的 css 文件控制效果，mdx 文件保存数据，你可以随便改动 css 文件来调整视觉效果，上面截图是 GoldenDict 里 css 版的默认画面。

![](https://skywind3000.github.io/images/blog/2017/dict/dict11.png)

#### 词典下载

- 度盘：`s/1hsopeRy` （防止扫描请自己在前面拼接 `https://pan.baidu.com/` ）。
- Github：[skywind3000/ECDICT-ultimate](https://github.com/skywind3000/ECDICT-ultimate/releases/tag/1.0.0)。

内容包含：

- MDX 版本（及去音标版）：支持 GoldenDict / mdict / BlueDict
- 欧陆 Eudic 版（及去音标版）：欧陆词典（桌面，手机）
- Kindle 版本
- MDX CSS 美化版本：支持 GoldenDict / mdict / BlueDict
- StarDict 版本：支持 StarDict，多看系统

#### 常见问题

**Q：电脑桌面用户用什么词典软件来挂载《简明英汉必应版》？**

首推使用 GoldenDict ，次选欧陆或者 mdict，配套 mdx 格式的数据库，GoldenDict 用户不要使用老旧的 1.0，请使用 1.5 以后版本才支持 mdx 词典格式：

- [GoldenDict for Windows](https://github.com/goldendict/goldendict/releases)
- [GoldenDict for Mac OS X](https://github.com/goldendict/goldendict/wiki/Early-Access-Builds-for-Mac-OS-X)
- [GoldenDict for Linux](https://github.com/goldendict/goldendict/wiki/Early-Access-Builds-for-Linux-Portable)

把词典 mdx 文件放到 GoldenDict 安装目录下的 content 目录即可，或者放在其他地方，在 GoldenDict 里面设置下路径即可。

**Q：手机用户用什么词典软件？**

欧陆和 BlueDict ，注意欧陆请用原版 eudic 格式，BlueDict 请关闭 strip word。否则你查 taut，可能会查出：taut, taut-, taut., -taut , 以及 taut. (后面有一点) 这么多单词出来，他们 strip 过后都是 taut，具体先显示哪个，这是字典软件决定的。

**Q：我用手机欧陆词典搭配 CSS 美化版连 estate 都查不出来？**

这是欧陆词典对 mdx支持不好，有 bug，我跟欧陆联系过，欧陆客服的反馈：

> 这个问题主要是因为你的扩充词库里面包含了一个特殊的单词"Estārm" ，所以导致检索失败。我们这边会改进下，下个版本可以解决。

结果等了半年多，欧陆还是没有修正，不当如此，欧陆还有 strip word 的顺序问题，所以欧陆词典没法使用 mdx 格式的 css 美化版，只能使用欧陆专版 eudic 格式，桌面系统使用 css 版本请安装 GoldenDict ，这是最佳搭配。

**Q：欧陆专用版有可能增加 CSS 支持么？**

个人时间问题，不太有精力去搞欧陆的 CSS，感兴趣可以自己搞，这个 MDX版本的 CSS 就是其他网友帮做的。再者手机屏幕就小，欧陆整体又比较素雅，所以我自己手机上是用欧陆专版（去音标词头版本），简洁明了。

**Q：我的 Kindle 刷了多看系统，可以用本词典么？**

可以，虽然我没刷过多看系统，刚才随便搜索了一下，多看系统支持 stardict 格式的词典，而本词典下载链接里，也有 stardict 格式。你还可以研究下多看系统是否支持原生的 mobi 格式词典，如果支持，那效果更好。

**Q：我看你只开源了《简明英汉增强版》的数据库，《必应版》数据库没开源？**

之所以没有在《增强版》上升级而选择重新发布一个词典主要是协议问题，《简明英汉增强版》数据是版权干净的，所以我开源，引用资料也是 MIT / GPL / Creative Common 等协议，所以我开源站得住脚。

《简明英汉增强版》/ ECDICT 项目就是给软件内需要内嵌词典又没有词典数据的开发者随意使用的，正常用也已经很多了（340万词条）。

你实在需要《必应版》的数据，可以从 mdx 逆向解出来

（有工具），比如 css 版本，解开每个单词都是 html，里面各项释义都是写好 tag 的，十分方便解析。

**Q：《简明英汉必应版》只有个简明释义，能否增加例句？或者详细解释？**

本词典目的是名字就叫 “简明”，追求的是快速查词 和 查得率，让你在最短的时间内掌握一个单词的基本含义。这是个人业余时间做的，你要我添加例句，实在超出我个人能力范围了，要看例句你可以看《21世纪》看《朗文》《牛津》啊，上面的例句多权威。

再者本词典可以方便的同其他词典一起搭配使用，在 GoldenDict 里，你加载了多个词典的话，查一个词 GoldenDict 会同时显示多个词典的释义：

![](https://skywind3000.github.io/images/blog/2017/dict/dict11.png)

GoldenDict 里查询 precept 单词，窗口中从上倒下分别显示了：

《简明英汉必应版》，《单词释义比例》，《朗文当代》，《剑桥高阶》，《有道同义词》和《英语单词说文解字》。

我的 GoldenDict 里面正在使用的词典有20+部（上面只展示了一小部分），一次输入，全部展示，多种词典搭配使用，比什么线上词典都强大太多了。

**Q：这个《英汉版》不错能否出《汉英版》？**

汉英词典请使用 CEDICT （开源词典），和 GoldenDict 对词典文件的全文搜索功能。

**Q：的确收录了不少短语，但是除了释义外，如何查询具体短语的用法？**

请继续搭配其他词典，和善用 GoldenDict 的全文搜索功能，正则表达式全文索引你所有大部头词典的所有文字（基本全是例句），这是最有效率的方法。

**Q：我不喜欢看《英汉词典》有没有纯《英-英》版本的收词量多的简明词典？**

只看《英-英》不看《英-汉》，这叫纯粹扯淡，请使用《简明英汉》配合你的纯英英词典，这是最有效率最节省时间的方式，举个例子你们就明白了：

牛津高阶：

> a large heavy animal with very thick skin and either one or two horns on its nose, that lives in Africa and Asia

朗文：

> a large heavy animal with very thick skin and either one or two horns on its nose, that lives in Africa and Asia

麦克米伦：

> a large animal with very thick gray skin and one or two horns on its nose. It lives mainly in southern Asia and Africa.

简明英汉：

> 犀牛

碰到生词如果只看英文释义看起来篇幅大不说，还有点打哑谜的感觉。还是结合简明释义看效率高点，没中文释义的话，心里没底，可能我看懂了英文释义，但是不太确定是否真的看懂；或者我理解错了，却以为自己理解对了；或者即便我看懂了，以后看到中文也不知道英文对应的是啥。

所以搭配使用各种词典，让你事半功倍，从更多方面了解一个单词，让你脑回路更多的链接起来。


**Q：本词典制作使用了哪些工具？**

开发语言用的 Python，以及 beautifulsoup4, lxml, requests 等常用模块，自然语言处理用到了 WordNet 和 NodeBox 两个包。

我开源的 ECDICT 项目（Python 词典数据库及相关脚本），以及其他自己写的包括自然语言处理，BNC / COCA 的分析程序，十多个不同类型的爬虫，等大大小小几十个脚本程序。

数据库使用 SQLite，CSV 等。

（完）



PS：生命的价值，在于奉献

