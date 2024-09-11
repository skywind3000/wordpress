---
uuid: 2472
title: 256字节3D程序是如何实现3D引擎的呢？
status: publish
categories: 图形编程
tags: 图形
date: 2016-08-26 22:52
slug: 
---
网上有很多 256 个字节实现图形渲染的 "引擎"，他们的原理是什么呢？

1. 全都不是基于正统3D引擎的多边形绘制，而是基于少数特定情况的简化版光线跟踪算法
2. 只能渲染特定几种物体，并不能渲染通用物体。
3. 无资源或者少资源（基本靠生成），重复
4. 16位代码，COM格式的可执行（没有PE头，代码数据和栈都在一个段内，指针只有两字节）
5. 尽可能用汇编来写

你自己花点时间也能做出来，

具体解释一下：

简化版的 raycasting，实现起来的代码量比通用的多边形绘制方法至少 N个量级。

基本的光线跟踪，在 320x200 的解析度下，从摄像机中心射出 320x200条光线，屏幕上每个点对应一条光线，首先碰撞到的物体的位置颜色，就是屏幕上这个点的颜色：

![](http://skywind3000.github.io/word/images/2016/3d-256-1.jpg)

可以描述为下面这段代码：

```cpp
for (int y = 0; y < 200; y++) {
    for (int x = 0; x < 320; x++) {
        DWORD color = RayCasting(x, y); 
        DrawPixel(x, y, color);
    }
}
```

其中函数 RayCasting(x, y) 就是计算从视点开始穿过屏幕上 （x, y）这个点的射线。

所谓简化版的光线跟踪，是只需要实现特定物体，以及针对特定条件，比如早年游戏里面用的最多的实时光线跟踪绘制地形高度图的（比如三角洲特种部队，xxx直升飞机）：

![](http://skywind3000.github.io/word/images/2016/3d-256-2.jpg)

比如云风 2002年写过的文章：[3D地表生成及渲染 (VOXEL)](https://dev.gameres.com/Program/Visual/3D/Voxel.htm)
实现上述效果的地形渲染，只需要 200多行 C 代码
使用标准三角形渲染这样的地形（软件渲染），代码少说也上千行了，使用标准的光线跟踪少说也要 500行左右。

<!--more-->

但是，我们情况比较特殊：

1. 只渲染地形（高度图）
2. 视角采用水平视角（可以象 doom一样左右转动，前后移动，但是不能偏头）

光线跟踪的流程可以针对这种情况大大简化：

![](http://skywind3000.github.io/word/images/2016/3d-256-3.jpg)

（高度图，白色表示高的地方，黑色表示矮的地方）

![](http://skywind3000.github.io/word/images/2016/3d-256-4.jpg)

由于高度图的特殊性以及彩用水平视角，屏幕上同一列光线可以只算一条：

![](http://skywind3000.github.io/word/images/2016/3d-256-5.jpg)

没错，从屏幕最左边一列列的向右边绘制，每一列只需要先从最下方的光线寻找碰撞，找到碰撞以后，就逐步沿山体爬坡，计算出同一列其他光线的交点，这样的光线跟踪虽然效果看起来还行，最终代码写起来也就200行（C代码），用16位汇编紧凑点来写，256个字节未尝不可。

嗯，好吧，其实云风是参考 flipcode 上的这篇文章：
[flipcode - Realtime Voxel Landscape Engines](http://www.flipcode.com/archives/Realtime_Voxel_Landscape_Engines-Part_2_Rendering_the_Landscapes_Structure.shtml)

有人用flash实现了一遍，直接可以在浏览器上看效果：
http://www.unitzeroone.com/flex_2/voxel_landscape/

另一个著名的例子就是类《重返德军总部》，《DOOM》里面用到的光线追踪：

![](http://skywind3000.github.io/word/images/2016/3d-256-7.jpg)

这是 Javascript 实现的类 DOOM 引擎，只有 265行 js代码：

[A first-person engine in 265 lines](http://www.playfuljs.com/a-first-person-engine-in-265-lines/) （文章）

这种地牢渲染情况也比较特殊：
1. 只渲染三种物体：墙壁，地面，天花板，
2. 同样采用水平视角

先画地面和天花板：也是从屏幕最下面投射一次性投射出一排光线出去，相交到地面（或天花板）上的某一行。

![](http://skywind3000.github.io/word/images/2016/3d-256-8.jpg)

从屏幕最下面那一行像素开始，计算那一排光线投射后相交于地面上的线段（x1,y1）-（x2,y2），代表代表地面上相交线段左右两边的端点，然后根据屏幕宽度缩放着绘制过去。

接着绘制墙壁，从坐到有右判断交点就是了，一竖条一竖条的绘制：

![](http://skywind3000.github.io/word/images/2016/3d-256-9.jpg)

![](http://skywind3000.github.io/word/images/2016/3d-256-10.jpg)

注意处理远小近大（除以z 来决定这一竖条墙壁的缩放比例）：

![](http://skywind3000.github.io/word/images/2016/3d-256-11.jpg)

早年不少地牢类 FPS游戏使用这个方法，实现起来也十分精简（javascript 才 265行）上面的几个例子，都是使用简化过的 raycasting 进行渲染：

1. 针对特定物体：地形，墙，地板 等
2. 采用水平视角（不能歪头）

通过这种简化，光线路径计算十分的简单，不管是 C实现 或者 javascript/ flash 实现，代码基本可以控制在 200行内。

来看第一个例子：

![](http://skywind3000.github.io/word/images/2016/3d-256-12.jpg)

明显的光线跟踪，只需要实现对一种特定的数学曲线/面的碰撞检测即可，颜色使用黄色，用交点的法向确定下明暗即可，效果十分平滑。
然而，代码尺寸限制，它只能绘制这种数学曲线/面，并不能绘制其他形状的东西，所以并不能称为引擎。

来看另一个例子：

![](http://skywind3000.github.io/word/images/2016/3d-256-13.jpg)

这个墙面只有两种类型（横的或者竖的），由于性能可以不用考虑太多，
可以比 doom的例子更简化一点，只对三种平面求焦点：

1. 地面或者天花板（z=-1，z=1）
2. 横墙：x坐标不变
3. 竖墙：y坐标不变

算起来应该也很快，C实现的代码量有可能控制在150行左右。

接下来是代码压缩了，选择 .COM的可执行格式，它没有 PE头，纯代码+数据，同时SP, ES, DS, CS 等四个段寄存器都是指向同一个数据段，所有数据都用 16位 near 指针访问（2字节）。

最后手工重构成汇编版本（C编译器产生的代码实在太庞大了），如果有资源，用256色（8位）或者16色（4位）， 并且使用 RLE压缩（解压代码很短），或者代码动态生成资源。

我以前也用纯汇编实现过一个 1KB 左右的完整空战游戏，16位的手写汇编，100字节就能做好多事情了，按照上面的简化版 raycasting ，逻辑比空战游戏简单不少。

通过不断的简化绘制模型，增加限制，以及不断的代码优化，
256个字节内实现题主图中的几个 demo应该是可以的。

相关阅读：

[计算机底层是如何访问显卡的？](http://www.skywind.me/blog/archives/1774)

[如何写一个软件渲染器](http://www.skywind.me/blog/archives/1498)

