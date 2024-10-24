---
uuid: 2594
title: OpenGL / DirectX 如何在知道顶点的情况下得到像素位置？
status: publish
categories: 图形编程
tags: 图形
slug: 
date: 2020-08-13 18:21
---
DirectX 和 OpenGL 是如何得知对应屏幕空间对应的纹理坐标和顶点色的呢？一句话回答就是光栅化。具体一点，实现的话，一般有两种方法：Edge Walking 和 Edge Equation。

两个我都完整实现过，下面分别介绍下具体原理：


#### Edge Walking

基本上所有基于 CPU 的软件渲染器都使用 Edge Walking 进行求解，因为计算量少，但是逻辑又相对复杂一点，适合 CPU 计算。具体做法分为三个阶段：

**第一阶段**：拆分三角形，将一个三角形拆分成上下两个平底梯形（或者一个），每个梯形由左右两条边和上下两条水平线（上底，下底）表示。

![](https://skywind3000.github.io/images/p/renderhelp/raster_1.jpg)

普通三角形可以拆分成上下两个平底三角形，不管是上面的那一半还是下面的那一半，都可以用一个平底梯形来表示（即上底 y 值 和下底 y 值，以及左右两边的线段），这样再送入统一的逻辑中渲染具体某一个平底梯形。

**第二阶段**：按行迭代，然后以梯形为单位进行渲染，先从左右两条边开始，一行一行的往下迭代，每迭代一次，y坐标下移1像素，先根据左右两边线段的端点计算出左右两边线段与水平线 y 的交点：

![](https://skywind3000.github.io/images/p/renderhelp/raster_2.jpg)

然后继续插值出左右两边交点的纹理坐标，RGB 值 之类的 varying 型变量，然后进入扫描线绘制阶段。

**第三阶段**：按像素迭代，有了上面步骤计算出来的一条水平线，以及左右端点的各种 varying 变量的值，那么就进入一个 draw_scanline 的紧凑循环，按点进行插值，相当于 fragment shader 干的事情。

计算 varying 变量插值的时候需要进行透视矫正，根据平面方程和透视投影公式，可以证明屏幕空间内的像素和 1/w 是线性相关的，而三维空间的 x / w, y / w, z / w 和屏幕空间也是线性相关的，也即各个 varying 变量按屏幕空间插值时需要先 / w，然后按照屏幕空间每迭代一个点时再除以最新的（1/w）就可以还原改点的真实 varying 变量值。

完整实现可以参考我写的 700 行软件渲染器：

- [如何写一个软件渲染器？](/blog/archives/1498)

而对于透视矫正的数学原理不清楚可以看《[透视矫正原理](/blog/archives/1828)》这篇文章。

上面是第一种方法。

#### Edge Equation

这个方法简单粗暴，虽然计算量较大，但是计算方法简洁而单一，适合 GPU 实现，即按照三角形外接矩形（或者屏幕上任意矩形），两层 for 循环迭代每一个一个像素，先走一遍 Edge Equation 判断是否再三角形范围内，如果否的话就跳出，如果是的话，使用插值方式得到各个 varying 变量的值（纹理坐标，RGB顶点色和法线等）。

由于没有像 Edge Walking 一样迭代左右两边的每个像素，所以插值使用了一种“重心坐标”的公式，直接参考三个顶点的位置和当前点重心坐标来插值：(点击 Read more 展开)

<!--more-->

![](https://skywind3000.github.io/images/p/renderhelp/raster_3.jpg)

通过计算 A/B/C 三个子三角形面积同大三角形面积的比例，计算出重心坐标的三个常数 a, b, c，又通过 a, b, c 插值得到该点各个 varying 变量的值，计算细节可以参考 opengl spec 或者 [vulkan spec](https://vulkan.lunarg.com/doc/view/1.0.33.0/linux/vkspec.chunked/ch24s07.html) ：

![](https://skywind3000.github.io/images/p/renderhelp/raster_4.png)

两层 for 循环迭代矩形里每个点，然后判断在三角形内的话，就用上面的重心公式插值得到 varying 变量的值，计算量虽然比 edge walking 大很多，但是形式单一，没有分支，适合 GPU 实现。具体实现上优化也很多，比如可以只在端点处用重心公式插值出端点的 varying 变量，而中间的点，可以用 1/w 的 edge walking 方式进行插值计算，提高效率。

由于该方法天生适合并行处理，比如用网格将 1280x1024 的屏幕按照 32x32 的网格分成 40x32 个矩形 tile，每个矩形由一个硬件计算单元负责，提交三角形时，先判断三角形覆盖到了那几个 tile，然后同时让负责这几个 tile 的计算单元同时工作，每个计算单元负责按照上面的流程迭代自己矩形内部的所有点，将三角形落在该矩形范围内的部分绘制出来，多个计算单元可以独立渲染，不互相干扰。

所以显卡就是可以很多个计算单元并行干这类傻重粗的活计，即便当前分辨率 x 4 倍抗锯齿的活计也能接得下来。

相关实现可以参考：

- [如何使用 C++ 写一个可编程软件渲染器？](/blog/archives/2589)

感兴趣可以继续阅读相关资料。

#### 更多阅读

- [3D 图形光栅化的透视校正问题](/blog/archives/1828)
- [计算机底层是如何访问显卡的？](/blog/archives/1774)


