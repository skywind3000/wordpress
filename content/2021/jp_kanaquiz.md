---
uuid: 2602
title: 我在命令行下学日语
status: publish
categories: 大浪淘沙
tags: 随笔
slug: 
date: 2021-12-24 02:04
---
同一个动作重复 300 遍，肌肉就会有记忆，重复 600 遍，脊柱就会有记忆，学完五十音图不熟练，经常遗忘或者要好几秒才想得起来一个怎么办？没关系，我做了个命令行下的小游戏 [KanaQuiz](https://github.com/skywind3000/KanaQuiz) 来帮助你记忆：

```text
usage python3 kanaquiz.py <operation>
operations: 
    python3 kanaquiz.py {-h}     play hiragana only
    python3 kanaquiz.py {-k}     play katakana only
    python3 kanaquiz.py {-a}     play all kana quiz
    python3 kanaquiz.py {-d}     play dakuon quiz
    python3 kanaquiz.py {-t}     play trinity quiz
    python3 kanaquiz.py {-l}     list kanas with romaji
    python3 kanaquiz.py {-o}     list kanas only
    python3 kanaquiz.py {-q}     query performance history
```

首先使用 `-l` 参数来复习所有假名：

```bash
python3 kanaquiz.py -l
```

然后在终端中查看：

![](https://skywind3000.github.io/images/blog/2021/kana_1.jpg)

当你复习完了，可以用下面命令开始挑战：（点击 Read more 展开）

<!--more-->

```bash
python3 kanaquiz.py -h
```

其中 `-h` 也可以换成 `-k` ，然后终端里会出现：

```
[ よ ]  (1/46)
 ? {光标}
```

学习规则类似 anki 卡片，上面显示要复习的假名，下面你需要用尽快的速度输入它的罗马音，然后回车继续

![](https://skywind3000.github.io/images/blog/2021/kana_2.jpg)

每输入完一个，会有时间统计，看你用了多长时间，完成挑战后，会有一份漂亮的战绩报告：

![](https://skywind3000.github.io/images/blog/2021/kana_3.jpg)

用来告诉你哪些假名你很熟练，但是哪些你还是不够熟悉，需要多加练习，这样，在终端里工作累了，可以随时挑战一下，发现自己的不足，同时每天能看得到自己的进步。

理论上看到每个假名你至少 1 秒以内要能反应出它的读音才行，当然越快越好，所以成绩报表里，一秒钟是绿色，颜色越浅代表越熟练，反之代表越生疏。

可以用：

```bash
python3 kanaquiz.py -q
```

随时查看你的历史成绩，了解自己的进步。

欢迎尝试：

- https://github.com/skywind3000/KanaQuiz

