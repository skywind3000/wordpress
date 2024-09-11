"=========== Meta ============
"StrID : 1951
"Title : Emacs/Vim 深度比较
"Slug  : 
"Cats  : 随笔
"Tags  : Vim
"=============================
"EditType   : post
"EditFormat : Markdown
"TextAttach : 
"========== Content ==========
生命在于折腾，折腾完了 Atom Editor，开始跟着陈斌大婶和 purcell的配置折腾 Emacs，比较下。很多人都在比较键位，比较插件，这是十分肤浅的，我们比较点深入的东西：

**代码结构**

- Emacs 源代码：eLisp 79%, C 21% 
- Vim 源代码：C 52%, VimScript 48%

从代码结构上来讲，Emacs的代码最多的是 elisp，C代码只是一个微内核，Vim 里C代码还是大头。当然不排除 24.X, 25.X以后 Emacs源代码里带了好几个重量级的包，而 Vim向来比较精简一些，官方没带啥大点的插件有关。去除自带插件后，Emacs的 elisp代码比例应该会下降很多，不过总体来说，Emacs有更多组件使用 elisp开发而成，也就是说可以被用户修改或者替换的地方比 Vim要多，当然速度也会相应慢一点（比如 Emacs新打开上万行的文件连续按住PageDown时cpu 100%占满），不过比较大 JB，Atom Editor来说，还是快不少。

**系统接口**

大框架基本类似：

- Vim 可以操作： buffer, window, tabpage, 光标，marker, region 跳转表等等。
- Emacs 可以操作：buffer, window, frame, 光标，marker，region 异步进程 等等。

Vim 有 local，Emacs有 mode，Vim有事件触发，Emacs有各种钩子，基本大框架类似的。

键位设置也都很灵活，会配置的话，可以把 Emacs键位全部弄成 Vim的，比如 Evil，或者Vim里面也可以配制成进去就自动进入插入模式，全部用 Emacs键位。

具体到比如 buffer 或者窗口里面，Emacs的窗口或者 buffer /window 属性更多一些，Vim也有一些 Emacs没有的基础设施，比如 jumplist, quickfix之类的，不过 Emacs也可以用插件实现，实现 jumplist没问题，比较独立，但每个插件实现一个类似的 quickfix的东西，实在是比较蛋疼。

**脚本语言**

VimScript 类似 Lua，但更啰嗦些，没啥好说的，要上手可能就是2-3天的样子，主要是实际编写中熟悉各种 Vim内部结构体系，以及api。

EmacsLisp 类似 clisp，稍微有些区别而已。clisp中的向量： (vector 1 2 3 4) 在 elisp中可以用中括号来表示：[1 2 3 4] 这样对减少小括号数量有一些帮助，代码读起来没那么拗口，可惜实际写 elisp的过程中，向量用的并不多，各种插件用的最多的还是 list，alist，plist 几种容器，小括号还是满天飞，如果不借助编辑器的匹配，缩进，还有彩虹括号（不同层次的括号用不同颜色的小插件）代码很难阅读，自己写好写点，看别人代码要对括号对半天（特别是他们把很多写一行的话）。

Lisp变量可视范围比较好用，局部变量可以 “遮盖住” 全局变量，比如你在 VimScript里面要临时跳转到一个新目录需要这么写：

```text
let cd = haslocaldir()? "cd" : "lcd"
let saved = getcwd()
silent! exec cd "my new directory"
......
silent! exec cd saved
```

而 elisp里面，利用局部变量遮盖特性，简单的：

```text
(let ((default-directory "my new directory"))
  .....
  )
```

在这个 let的作用范围内，buffer的全局变量 `default-directory` 被新定义的同名局部变量给遮盖住了，里面的代码（包括调用外面定义的函数）取这个名字的变量，都会取到你新定义的变量，作用范围结束就恢复了，这样比 vimscript方便不少，类似的用法还有 `(with-selected-window new-window...)` 把当前窗口设置成 new-window并做一些事情，当离开代码作用域以后，自动恢复成先前的窗口，如果VimScript来做这事情，又需要保存前窗口，然后跳转，最后又恢复。

VimScript在 vim6.0及以前的时代里比 EmacsLisp弱很多，连个 List，HashTable之类的容器都没有，怎么写复杂的程序嘛，Vim7.0以后补充了字典和列表还有三元式，简单面向对象等，终于可以写点复杂的东西了，而 Vim下很多传奇性的插件，其实也正是 7.0以后才出现的。Vim8.0以后又进一步补充了匿名函数和 partial function (类似简陋版的 curry 函数）等等特性，除了啰嗦外，写点复杂东西问题不大，比如前久有人用 VimScript写了一个 C编译器，可以在Vim里跑 C脚本。

Lisp里面的宏类似C++模版加强版，C++模版只有一层，定义好模版，然后生成代码。Lisp的宏可以先用程序生成模版，再由模版生成代码，类似模版的模版。不过实际使用中，为了不让自己的代码飞的太远，难以维护，大部分插件开发者在 elisp里面最多就是 require一下 common lisp的兼容包，用一些 common lisp里面诸如 loop, for, incf, case 之类的通用宏，自己定义也限于定义一些小工具，没有人丧心病狂的搞一些影响程序结构的东西，定义成另外一门语言。

大部分插件开发者实际上还是把它当作充满括号的 lua 来用，除去一些便利性外，麻烦也还是挺多的。

**异步进程**

早期的 Vim没有异步进程操作，导致很多插件没有 Emacs那么顺畅，比如生成 tag或者编译，Vim只有傻等着，Emacs可以同时做其他事情，Vim8.0以后异步接口和后台时钟等也比较完善了，假以时日各大常见插件能逐步发挥 8.0特性的时候，相信也能带来一致的体验，包括纯vimscript实现的 shell，以及 gdb集成，发邮件等，问题不大。

<!--more-->

实际使用中最紧缺的异步任务，虽然系统都支持，但是显然就插件来讲，Vim的插件跟进的速度还有待提高，毕竟本身已经晚出了那么多年了。不过好在自己可以撸，熟悉 VimScript的话，可以把最紧缺的 tag 生成，编译， grep等几项日常使用频率最高的工作自己写插件异步化了，比如我自己撸的：
[skywind3000/asyncrun.vim](https://github.com/skywind3000/asyncrun.vim)

Vim里面的 CtrlP（模糊文件查找），还有 tagbar（文件符号列表），先前用起来就是一个字 “卡”，经常卡住做不了别的事情。同比之下，Emacs的 Helm系列全家桶做文件模糊查找就顺畅的多。同样的 python实时补全插件 jedi，在 Vim下会卡，Emacs下很流畅也是这个原因。好在最新版的 CtrlP已经增加了异步任务支持，可以后台检索文件，是没卡界面了，但是确实还需要时间进一步完善改bug。

Emacs的 flycheck 被人津津乐道，方便的后台异步检查当前编辑文件的语法，并且标注出错的地方。Vim的同类产品 syntastic 以往会把界面卡住，你需要停下编辑，等着跑 lint跑完了以后它才给你标注出来。所以很多人比较了 flycheck以后，觉得 flycheck很爽，一边写着，前面出错的地方就会被自动标注，根本不用停下来，于是坚定不移的转战了 Emacs了。当然，Vim8.0以后也出现了自己的异步检查插件：[w0rp/ale](https://github.com/w0rp/ale) 。

总体来说，目前异步进程两大编辑器支持都差不多了，但原有非异步的 Vim的各大著名插件，还需要进一步跟进完善，才能提供更好的体验。

**界面分离**

Emacs 和 Vim都支持 client/server 模式，但是不是一回事情，Vim的 client/server就是简单的给做服务的 Vim实例发一些消息，执行一些代码，client控制 server打开一些文件而已。

Emacs的 client/server是真的 client/server，界面和内在逻辑相分离，你可以在 GUI的 Emacs里面打开一堆文件，并在命令行版本的 Emacs里面链接到 server里面来共享多个buffer和状态，同时编辑，还可以在 Emacs上面套一个壳，遵守一致通信协议下，完全用 Electron来写个现代界面。

NeoVim里面提供了类似的支持，界面逻辑相分离，而且比 Emacs更进一步做了一个更漂亮一点的界面系统，比如有人用 Electron 给 NeoVim做了一套 GUI，前台是 javascript做的界面，后台是NeoVim跑的逻辑：[extr0py/oni](https://github.com/extr0py/oni)

这个做的十分漂亮只能希望 Vim早点支持，把 NeoVim那部分界面 patch给收录了。

**org-mode**

org-mode适合用来安排 GTD，写文档，整理思路之类的，Vim下面确实没有可以代替的插件，有个vim-org-mode，实现的不伦不类的（[vimoutliner/vimoutliner](https://github.com/vimoutliner/vimoutliner) 比 vim-org-mode 更好一些）。

不过说道很多人对 org模式赞不绝口的 GTD，我多两句嘴，但凡用过现代 GTD软件的，基本不会去用 org-mode的 gtd，现在 GTD管理基本都在手机上做了，同时支持多端同步，手机采集素材和临时想法（包括不限于文字，照片，录音），PC上用PC版或者 Web版整理编辑日程，日常在手机上随时同步查看 next action，这才是 GTD的正确用法，我不知道各位 org 深度用户抱着 org的 gtd不放干嘛？是有一些同步 org 日程的方法，但都较为山寨又缺乏统一体验。

GTD 和各种 知识/碎片收集整理的方法，我们还是使用各种多端同步的现代化解决方案吧。

**其他优势**

Emacs GUI版本可以显示图形，Vim这个就没法了。Emacs Lisp 新版本支持多线程和 FFI，可以调用外部动态库。VimScript没有这个能力，需要借助 Python来做类似的事情。

**最终比较**

喜欢一个编辑器和喜欢一个人差不多，有的女的喜欢上一个男的，可能因为他的手长的比较好看，或者那天下午阳光明媚，他穿了一件白衬衫。

我不喜欢 Emacs的地方，是窗口/Frame管理，十分猥琐：


1. Emacs 的 `Frame` 比 Vim 的 `TabPage` 功能类似，但是 Emacs的 Frame确实比 Vim的 `TabPage` 麻烦很多，比如 GUI下面每个 Emacs的 `Frame` 就是一个新窗口，而每个 GVim的 `TabPage` 是一个GUI上的 TAB。Emacs的这个设置相当恶心，Vim下我可以设置 ALT_1234来快速切换各个 `tabpage`，而 Emacs如果这么做，GUI下面窗口用热键跳来跳去，你就会觉得相当怪异。直到现在Emacs的 `Frame` 用的人也不多，而 Vim的 `TabPage` 确实十分顺手，这点不是插件可以解决的。

2. Buffer切换，Emacs下面更多是模糊查找切换buffer，原始或者 helm增强过的 c-x b，快捷键绑定的上一个 buffer或者下一个buffer。而 Vim中，我可以用ALT+数字来直接切tabpage，ALT+SHIFT+数字来直接快速切换buffer，emacs下有类似插件，但往往用emacs的时候各种buffer开的太多，切换起来真心累。

3. 我不喜欢正在编辑的文档或当前正在引用对照的文档被 emacs的某些插件随时切换走，经常打开个 grep或者编译什么的，还在看得一个文档就没了。不用提醒我有独占窗口，Emacs的 reference我基本都快速过过一遍了，我当然知道 `(display-buffer ... )` 的时候有很多策略，窗口也可以设置成 dedicated window。我告诉你们问题在哪里，如果你不想文件被切走，你就只能把很多窗口设置成 dedicated window，而某插件想要显示自己时，粗暴的默认参数调用一下 `(display-buffer .. )` 或者 `(display-reuse-window ... )` 时，找不到可以显示自己的空间，Emacs就会默认帮他打开一个新的 frame，在GUI下面一个 frame是一个新的 Emacs窗口。所以你会觉得很诡异，用着用着，弹出一个新的 Emacs窗口来，真他妈的操蛋。这不是你的错，是 Frame机制和这些插件的问题。

4. 过分依赖ALT键，导致终端下支持不太好，我好几个 ALT键还想留给终端软件自己用呢，你全把我占完了，我不一次性把所有ALT隐射给你你还不能正常工作。Vim里面 ALT键很和谐，终端软件用一部分 ALT键快速操作跳转ssh窗口，Vim 自己用另外大部分补充 CTRL的不足，十分宽松舒适。

5. 缺乏统一标准，比如 Location list，对就是 Vim里面的 `Quickfix`和 llist之类的东西，就是我们普遍运行编译，grep，生成查找tag，lint的时候会出现很多文件和行号，`Quickfix`用来显示这些结果，选中一个就会跳转过去，这么一个东西。用 Emacs当然可以用插件实现一个，小 case，但是问题是：没有统一标准。各个插件都自己实现了一套，你编译时 emacs弹出一个窗口或者占用一个你的老窗口显示编译结果，你查找grep的时候，又弄出一个新窗口来显示结果，你查找tags的时候，还会再弄一个新窗口出来，所以 Emacs下面界面缺乏统一逻辑，有的插件新开窗口，有的插件替换窗口，窗口 buffer 满天飞。不停的开窗口，关窗口，切buffer。但 Vim下面有标准的 `Quickfix`，这些事情统统显示在下方 `Quickfix Window`中，标准统一，还有系统级别的 api来提供统一接口，还有相关配套插件来根据 quickfix内容在源代码上以高亮标志出来，十分整洁，这不是 Emacs没有能力这么做，而是 Emacs没有统一标准，导致成天开关各种窗口，经常切换buffer，是 Emacs里面的一项日常的日常，Vim里面你从来不会觉得这些事情是一个负担。类似缺乏标准的还有各种 jumplist, 界面规范等。所以 emacs里面经常你一套我一套，不得不靠一些 helm, company 等全家桶来提供统一的体验，然而治标不治本。

6. Vim 的 `bufferlist` 和预览窗口更好用一些，比如vim buffer list里面可以标注一个 `buflisted`的属性，我在浏览tags时，很多时候都是在 `preview window`里面预览一下，预览窗口里的文件默认是 `buflisted=0`的，不会污染我的buffer list，emacs下面预览文件一多，buffer list就乱了，你打开几个文件，还得一个个去 kill去，准确的说 emacs也可以用脚本实现一模一样的 `bufferlist`和 `preview window`（当然 Vim也可以脚本另实现一套 buflist+预览，还有上面的 `quickfix`只是没人这么做），但还是上面那句话，没有标准，你自己实现了，也没有任何插件支持，你也不可能把所有插件全改一遍，来统一他们的界面逻辑，总之就是界面逻辑难统一，工作流混乱。

不同的地方很多，这里也总结不完，但是大体就是这些，非要让用一句话形容 Emacs的话，那就是用 Emacs就像 SM，有的地方很爽，有的地方很疼。

嗯，折腾和试用结束，不是不强大，是不搭。
