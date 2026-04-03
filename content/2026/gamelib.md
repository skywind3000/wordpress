---
uuid: 3666
title: 单头文件 C++ 游戏开发库（GameLib.h）
status: publish
categories: 游戏开发
tags: 小游戏
slug: 
---
最近小孩在学 C++（信奥），学了堆语法以后不知道干嘛，学了一年也只会对着黑窗口打印内容，正反馈太弱了，不像其他语言，学个几天就能做出漂亮的东西来，恰巧他对开发游戏感兴趣，我扫了一眼现在 C++ 的游戏开发框架，都太复杂了，SDL 概念琐碎，SFML 使用麻烦，所以我写了个针对初学者的游戏库，只有一个头文件 `GameLib.h` 零依赖，拷贝到代码目录 `include` 就能用，十行代码就能出个小 demo：

![](https://skywind3000.github.io/images/p/gamelib/demo.png)

本着简化一切的思想，使用起来比 PyGame 还要简单：

```cpp
#include "GameLib.h"

int main() {
    GameLib game;
    game.Open(640, 480, "My Game", true);

    int x = 320, y = 240;

    while (!game.IsClosed()) {
        if (game.IsKeyDown(KEY_LEFT))  x -= 3;
        if (game.IsKeyDown(KEY_RIGHT)) x += 3;
        if (game.IsKeyDown(KEY_UP))    y -= 3;
        if (game.IsKeyDown(KEY_DOWN))  y += 3;

        game.Clear(COLOR_BLACK);
        game.FillCircle(x, y, 15, COLOR_CYAN);
        game.DrawText(10, 10, "Up/Down/Left/Right to move!", COLOR_WHITE);
        game.Update();
        game.WaitFrame(60);
    }
    return 0;
}
```

就这么几行代码，没有 SDL 里反锁的像素格式，消息机制，各种乱七八糟 SDL_ 开头的对象，也没有初始化就需要 500 行代码的 DirectX 那么麻烦，所有复杂的东西藏起来，只留下做游戏的乐趣。

编译：

```bash
g++ main.cpp -o game.exe
```

不需要加任何编译参数，很多初学者连命令行编译都不懂（比如我家小孩），只会直接在 DevC++ 里点编译+运行，让他们像用其他库一样添加一些类似 -ld3d9x 之类编译参数，可能直接就劝退一大群人，因此这个库完全使用默认编译参数，所有依赖都是动态库自己手工加载。

运行就能用方向键控制小球移动：

![](https://skywind3000.github.io/images/p/gamelib/demo1.png)

几行代码迅速看到反馈。

**为什么做这个库呢？**

市面上的游戏库（SDL、SFML、raylib）都很好，但对于刚接触 C++ 的初学者来说：

- SDL 要配置头文件路径、链接十几个 dll，使用复杂
- SFML 要用 CMake
- raylib 需要熟练掌握线性代数，三维图形基础知识，熟练 C/C++，对初学者太不友好

GameLib 的目标是零门槛：把 GameLib.h 拷到项目文件夹，写一个 .cpp 文件，点编译，游戏就跑起来了。

它专门为 Dev C++（很多学校编程课在用的 IDE）设计，兼容其自带的 GCC 4.9.2 编译器。当然，任何支持 C++11 的 Windows 编译器都可以用。

(点击下面展开更多)

<!--more-->

**特性一览**

零配置：

- 单个头文件 GameLib.h，拷贝即用
- 不依赖 SDL / SFML / DirectX / OpenGL
- 编译参数都不需要加（全动态加载），可选择性添加 -mwindows 参数
- 兼容 Dev C++ 自带的 GCC 4.9.2

开箱即用的绘图：

- 画点、线、矩形、圆、三角形（描边和填充）
- 内嵌 8x8 像素点阵字体，支持所有可打印 ASCII 字符
- DrawPrintf 像 printf 一样在屏幕上格式化输出
- 所有图形算法自行实现（Bresenham 直线、中点圆、扫描线填充）

精灵系统：

- 加载 PNG、JPG、BMP、GIF 等格式
- 支持 8-bit 调色板、24-bit、32-bit 图片（自动转换为 32 位 ARGB）
- 24 位图片自动补全 alpha 通道（设为不透明）
- 翻转、Color Key 透明、Alpha 混合、区域裁剪绘制
- 用整数 ID 管理，不需要理解指针和对象生命周期

键盘和鼠标：

- IsKeyDown — 按住检测
- IsKeyPressed — 单次按下检测（按下瞬间触发一次）
- 鼠标位置和三键状态
- 预定义所有常用按键常量：KEY_A~KEY_Z、方向键、F1~F12

声音：

- PlayWAV — 播放音效（WAV 格式，异步）
- PlayMusic / StopMusic — 播放背景音乐（MP3/MIDI，基于 MCI）
- 音效和音乐独立通道，互不干扰

游戏工具：

- Random(min, max) — 随机数
- RectOverlap / CircleOverlap — 碰撞检测
- Distance — 两点距离
- DrawGrid / FillCell — 网格绘制（适合俄罗斯方块、棋盘类游戏）
- GetDeltaTime / GetFPS — 帧时间和帧率

Tilemap 系统：

- CreateTilemap — 用 tileset 精灵创建瓦片地图
- SetTile / GetTile — 设置和读取瓦片
- DrawTilemap — 绘制地图，支持不透明、Color Key、Alpha 三种模式
- 只绘制屏幕可见范围内的瓦片，大地图也不卡
- 配合相机偏移轻松实现横版卷轴和视差滚动

**快速上手**

第一步：下载

把 `GameLib.h` 放到你的项目文件夹里。

第二步： 写代码

创建一个 main.cpp：

```cpp
#include "GameLib.h"

int main() {
    GameLib game;
    game.Open(800, 600, "Hello GameLib", true);

    while (!game.IsClosed()) {
        game.Clear(COLOR_DARK_BLUE);
        game.DrawTextScale(200, 250, "Hello, World!", COLOR_GOLD, 3);
        game.DrawText(280, 320, "Press ESC to exit", COLOR_GRAY);

        if (game.IsKeyPressed(KEY_ESCAPE)) break;

        game.Update();
        game.WaitFrame(60);
    }
    return 0;
}
```

第三步：编译运行

Dev C++：新建项目 > 添加 main.cpp > 编译运行。

或者命令行：

```bash
g++ -o game.exe main.cpp -mwindows
```

就行了。

**随机星空**

再来个有点视觉效果的例子，随机星空：

```cpp
#include "GameLib.h"

int main() {
    GameLib game;
    game.Open(800, 600, "Starfield", true);

    // 生成 200 颗星星
    int sx[200], sy[200], speed[200];
    uint32_t colors[] = {COLOR_WHITE, COLOR_LIGHT_GRAY, COLOR_YELLOW, COLOR_CYAN};
    for (int i = 0; i < 200; i++) {
        sx[i] = GameLib::Random(0, 799);
        sy[i] = GameLib::Random(0, 599);
        speed[i] = GameLib::Random(1, 5);
    }

    while (!game.IsClosed()) {
        game.Clear(COLOR_BLACK);

        for (int i = 0; i < 200; i++) {
            sx[i] -= speed[i];
            if (sx[i] < 0) {
                sx[i] = 800;
                sy[i] = GameLib::Random(0, 599);
            }
            game.SetPixel(sx[i], sy[i], colors[speed[i] % 4]);
        }

        game.DrawText(250, 290, "Press ESC to exit", COLOR_GRAY);
        if (game.IsKeyPressed(KEY_ESCAPE)) break;

        game.Update();
        game.WaitFrame(60);
    }
    return 0;
}
```

就这么简单，运行效果（点击播放 GIF 动画）：

![](https://skywind3000.github.io/images/p/gamelib/starfield.gif)

几行代码就能有看得见摸得着的东西，正反馈远远强过黑窗口打印文字。

这个 GameLib.h 适合开发哪些类型的游戏呢？

- 太空射击 (Space Shooter)
- 横版卷轴 (Side-Scrolling Platformer)
- 俄罗斯方块 (Tetris)
- 贪吃蛇 (Snake)
- 打砖块 (Breakout)
- 走迷宫 (Maze)
- 接水果 (Fruit Catcher)
- 弹幕游戏 (Bullet Hell)
- 画板程序 (Paint)
- 任何你能想到的 2D 小游戏

更多例子请访问项目主页：

https://github.com/skywind3000/GameLib


里面有 15 个例子程序，包括类似《打砖块》 ，《太空射击》之类游戏的代码：

![](https://skywind3000.github.io/images/p/gamelib/breakout.png)

一步一步教你从：窗口控制，键盘鼠标交互，图形绘制，精灵，音乐，卷轴等覆盖各个 GameLib.h 的功能点。

欢迎学会了 C++ 语法想做点什么的同学尝试。

