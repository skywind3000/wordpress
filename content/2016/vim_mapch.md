---
uuid: 1857
title: Vim 里如何映射 CTRL-h 为 left ?
status: publish
categories: 随笔
tags: vim
---
很多人习惯在配置文件中映射 CTRL+HJKL 为光标移动，却碰到了一些问题：

```vim
inoremap <c-h> <left>
inoremap <c-j> <down>
inoremap <c-k> <up>
inoremap <c-l> <right>
```

<c-h> 映射后无效或者映射以后按 `<BS>`键不能删除，这是什么原因呢？

很简单，因为你的终端软件（Xshell, SecureCRT）有些老，默认配置是按下`<BS>`键以后
发送的是：^H (ASCII 码 0x08），而 ^H在你的 Vim 里被你 inoremap 成 <LEFT> 了，所以你按了`<BS>`会被认为按下了左键。

早在 VT100终端时代，^H（ASCII码 0x08）表示`<BS>` 而 ^? （ASCII码 0x7f）表示`<DEL>`。过去 0x7f是留给 DELETE键使用的。而到了 VT220时代，DELETE已经变为 ^[[3~ （ASCII 码 0x1b, 0x5b, 0x33, 0x7e 共4个字节），而 ^? 的 0x7f 换给了我们的`<BS>`，有些老点版本的终端软件，默认 `<BS>`还是使用 VT100的 ^H，比如 Xshell 4 Build 0142以前的版本，默认`<BS>`是发送^H。SecureCRT直到6.x版本还在默认发送 VT100的 ^H。

你需要做的就是改一下终端默认配置而已，大部分不那么陈旧的终端软件，如今都是默认VT220的标准，比如 Xshell4 Build 0142及以后的 Xshell5，Putty，Mac下面的 Terminal.app, iTerm2，Ubuntu下面的 gnome-terminal，他们都是把 `<BS>` 发送成 ^?

你可以在你服务端下面查看下默认的键位设置：

```vim
$ stty -a
```

现在所有 Linux服务器的 erase （bs）基本都是 ^? 了（如果链接到非 Linux老操作系统 erase不是这个的话，需要改一下，可以在系统层改，也可以vim里面 set t_kb=...），Vim里面也是认可 ^?的，可老旧的终端软件却默认发送 ^H，不过好在他们都支持修改：

<!--more-->

**Xshell 老版本的修改方法**

![](https://skywind3000.github.io/images/blog/2016/vim_mapch_1.png)

Properties -> Terminal -> Keyboard 里，把`<BS>`设置成 127，而 `<DEL>`设置成 VT220 Del

**SecureCRT 6 的设置方法**

![](https://skywind3000.github.io/images/blog/2016/vim_mapch_2.png)

Session Options -> Terminal -> Emulation -> Mapped Keys, 勾选 Backspace sends delete

**Putty 设置方法**

![](https://skywind3000.github.io/images/blog/2016/vim_mapch_3.png)

好像默认是 ^? 的不过需要到：Configuration -> Terminal -> Keyboard 下面下确认下 The Backspace key 是 Control-? (127)

**Terminal.app**

![](https://skywind3000.github.io/images/blog/2016/vim_mapch_4.jpg)

Mac 下面的 Terminal.app 默认是发送 ^? 的，你也可以到 Profiles Advanced 下面确认下 “Delete sends Control-H” 没有勾选。

**iTerm2**

![](https://skywind3000.github.io/images/blog/2016/vim_mapch_5.png)

iTerm2 下面默认也是发送 ^? 的，可以到 Profiles -> Keys下面确认一下 “Delete key sends ^H” 没有被勾选。

**Gnome-Terminal**

至于 Gnome-Terminal 和 MinTTY之流的默认是 ^? 要修改可以看具体文本配置文件。

好了，默认 Vim 同时识别 ^H（ASCII 码 0x08）和 ^?（ASCII码 0x7f） 都把这两个当成`<BS>`，现在我们统一把终端软件的 `<BS>`改为 0x7f以后，^H 的 0x08就空出来给我们 noremap了：

```vim
noremap <C-h> <left>
noremap <C-j> <down>
noremap <C-k> <up>
noremap <C-l> <right>
inoremap <C-h> <left>
inoremap <C-j> <down>
inoremap <C-k> <up>
inoremap <C-l> <right>
cnoremap <c-h> <left>
cnoremap <c-j> <down>
cnoremap <c-k> <up>
cnoremap <c-l> <right>
```

其实这样映射是有好处的，有时候就想在插入模式下移动一小下，真没必要 <ESC>跳出。
命令模式下，这样移动也是有好处的，因为进场敲 Ex命令时都是按上，把上一条弄出来，移动下光标修改下，然后回车，这下 Ex命令模式下 直接 <C-k>把上一条显示出来，然后<c-h> 和<c-l>左右移动修改。当然你也可以map成 emacs格式，为了保持一致性，Command/Normal/Insert/Visual我都做了这个设置。

可能你会问，NORMAL下面的 <C-H> 之类的不是覆盖给窗口移动 <C-W>h 了么？这个看个人意愿了，比如你可以把你的窗口移动改为 <tab>h, <tab>j, <tab>k, <tab>l 四个键，向右移动窗口时normal下先按<TAB>再按L，多顺畅？

如果担心覆盖了原生 <c-h> <c-j> <c-l> <c-k>的话，我们看看原生这几个键是做啥的。

```vim
:help index
```

上面这条命令会列出 Vim里面所有默认按键的含义，平时推荐多看看：

	CTRL-H 同 `<BS>` 一样功能，我们都是直接用 `<BS>` 没人CTRL-H的，直接覆盖掉
	CTRL-J 同回车（有两个码 0x0d 或 0x0a），C-J是0x0d，硬回车是0x0a，没人按这个，覆盖。
	CTRL-K 输入 digraph，比如可以用来输入欧洲文字，不需要，实在需要可以把这个功能挪给 INSERT模式下的 CTRL-B （空闲），或者 <c-x><c-k> ，完全可以覆盖。
	CTRL-L 重绘，很少用，自己可以把他挪到 <leader>r 之类的键去多干净，覆盖。


好了，看看上面这四个键基本都是些无关痛痒的功能，完全可以覆盖之。

当然，对于需要用 `<C-K>` 进行 digraph 输入符号或者日文的同学，推荐改为 `<C-_>` (其实是CTRL和减号一起按下）：

    inoremap <c-_> <c-k>

好了，因为本来 `<C-_>` 是用来处理从右向左的文字的（阿拉伯语，希伯来语，波斯语）我们不需要，所以覆盖之用来输入符号，原来输入 `"<c-k>ko"` 插入的是 "こ" ，现在改成了 `"<c-_>ko"` 而已。

--
相关阅读：[Skywind Inside - Vim 中正确使用 Alt映射](http://www.skywind.me/blog/archives/1846)



