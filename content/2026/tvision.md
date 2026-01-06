---
uuid: 3656
title: C++ 最好用的 TUI 界面库 Turbo Vision 2.0
status: publish
categories: 编程技术
tags: 命令行
slug: 
---
说起文本模式界面库，也许有人听过 Turbo Vision 2.0，这货是当年 Borland C++ 3.1 （不是 Turbo C 2.0）背后的商用界面库 TV2 的开源版，经过多年迭代，如今是一款支持 unicode 和现代 C++ 跨平台的 TUI 库了：

![](https://skywind3000.github.io/images/blog/2026/tvision/tv2_intro.png)

项目地址：https://github.com/magiblot/tvision

主要特性：

- 跨平台：Windows，Linux，macOS，DOS，FreeBSD
- 支持鼠标，支持 unicode，正常显示中文；
- 多窗口：窗口可以自由拖拽移动，扩大缩小，全屏，互相覆盖（overlap）
- 控件多：主菜单，对话框，checkbox, radiobox，dropdown list，文件选择器，进度条，阴影
- 文本编辑：语法高亮，自动 indent，鼠标选中，shift+方向键选中，CTRL+C/CTRL+V
- 支持真彩：原来老的 Borland 版本的 TV2 只支持 16 色。

Linux 下大部分 TUI 程序都是平铺窗口，无法重叠，更无法自由拖动，而 Turbo Vision 2.0 完全像用图形界面程序一样，鼠标操作这些窗口自由移动，扩大缩小，全屏化：

<!--more-->

![](https://skywind3000.github.io/images/blog/2026/tvision/tv2_windows.png)

而且 Linux 下面大部分程序对 ALT+ ，CTRL+ ，SHIFT+CTRL+ 等组合键支持非常有限，而 TV2 对不同平台的键盘鼠标做了很好的兼容，让你在远程终端里也能自由的使用各种组合键和功能键。

用过 Borland C++ 3.1 的人一定会以为 BC31 重生了，某种意义上来讲是的，不要觉得技术古老，Linux 下面 TUI 发展几十年，没一个打得过 Turbo Vision 2 的：

![](https://skywind3000.github.io/images/blog/2026/tvision/tv2_term.png)

这是 TV2 做的终端模拟器 tvterm，各位天天用 tmux 分屏模拟，但 tmux 发展了那么长时间都不支持子窗口互相重叠覆盖，鼠标拖动，TV2 可以让你像用桌面软件一样灵活的操作各个子窗口。

Vim/NeoVim 直到 2019 年才支持 popup/floatwin 可以实现上面类似的效果，而 Turbo Vision 2 在三十年前就做到了。

过去 TV2 只支持 ANSI 编码，无法显示中文，如今中文，日文都能正常显示：

![](https://skywind3000.github.io/images/blog/2026/tvision/tv2_turbo.png)

包括 emoji：

![](https://skywind3000.github.io/images/blog/2026/tvision/tv2_emoji.png)

你在 Linux 下大部分 TUI 程序想调整下设置都只能编写配置文件，配置 vim 也只能写 vimrc，但 TV2 里有丰富的 TUI 设置对话框：

![](https://skywind3000.github.io/images/blog/2026/tvision/tv2_colors.png)

大部分设置，对话框里点点鼠标就能搞定，毫无学习门槛，无需看很多帮助才知道怎么写配置：

![](https://skywind3000.github.io/images/blog/2026/tvision/tv2_mouse.png)

当然 TV2 也有内置帮助系统，它有一套类似 .chm 等帮助系统，内部包含索引，跳转，可以在 TUI 内随时查看你的帮助文件，比如下面的快捷键帮助，基本上和 Windows 程序一脉相承：

![](https://skywind3000.github.io/images/blog/2026/tvision/tv2_help.png)

最后是编程接口，linux 下一堆 tui 接口，比如 ncurses 这样的都是比较初级的原始的，没有任何高级控件，同时接口也是 C 的，而 TV2.0 基本上所有高级控件你都可以直接使用，写起代码来类似传统的 Qt 程序：

```cpp
class HelloApp : public TApplication {
public:
    HelloApp();
    void showHelloDialog();
};

HelloApp::HelloApp() : 
    TProgInit(&TApplication::initStatusLine,
              &TApplication::initMenuBar,
              &TApplication::initDeskTop) {
    // 启动时显示对话框
    showHelloDialog();
}

void HelloApp::showHelloDialog() {
    // 创建对话框 (x, y, width, height)
    TDialog *dialog = new TDialog(TRect(0, 0, 40, 9), "Hello World");
    
    if (dialog) {
        // 居中对话框
        dialog->options |= ofCentered;
        
        // 添加 "Hello World" 静态文本 (居中显示)
        TStaticText *text = new TStaticText(
            TRect(2, 2, 38, 5), 
            "\003Hello World"  // \003 表示居中对齐
        );
        dialog->insert(text);
        
        // 添加 OK 按钮 (居中)
        TButton *button = new TButton(
            TRect(14, 5, 26, 7),
            "~O~K",
            cmOK,
            bfDefault
        );
        dialog->insert(button);
        
        // 显示模态对话框
        deskTop->execView(dialog);
        
        // 清理
        TObject::destroy(dialog);
    }
}

int main() {
    HelloApp app;
    app.run();
    app.shutDown();
    return 0;
}
```

基本就是类似 Qt 的编程方式：事件驱动+控件组合+OOP，不是 ncurses 那种 select/read 标准输入，自己解码半天终端控制码，在琐碎的控制各处显示，自己控制状态切换和重绘，写的你想吐。

Linux 下面基于 ncurses 二次封装的库也很多，但大多是个人项目，浅层封装，Turbo Vision 过去作为支持 Borland C++ 3.1 这种商用级 IDE 的界面库，不是这些玩票项目可以比得了的。

编程语言 TMBASIC 也是用 Turbo Vision 2 做的界面：

![](https://skywind3000.github.io/images/blog/2026/tvision/tv2_basic.png)

补充点历史，Turbo Vision 最初是 Borland 公司用 Pascal 实现的，用于 Turbo Pascal，后来在做 Borland C++ 3.x 的时候用 C++ 重新实现了一个版本，用于支持 BC31 的界面，在 BC31 里包含头文件和静态库，你可以直接用它构建 TUI 程序，接着 Borland 在 1997 年将 C++ 版本的完全开源了，就是我们上面说的这套的源头；

而 Pascal 版本的 Turbo Vision 一直没开源，Free Pascal 后面又根据 C++ 开源的版本重新实现了一套叫做 Free Vision 的界面库给 Free Pascal 做 IDE 用：

![](https://skywind3000.github.io/images/blog/2026/tvision/tv2_pascal.png)

我很喜欢它的设置界面，根本不用读文档写配置文件，直接对话框里全部帮你归好类了：

c
是不是很眼熟？Free Pascal 的 IDE，背后使用的 Free Vision，和上面的 Turbo Vision 同出一源。


PS：Turbo Vision 还出过几本书：

![](https://skywind3000.github.io/images/blog/2026/tvision/tvision1.jpg)

想看的话到开头项目主页里有链接。

