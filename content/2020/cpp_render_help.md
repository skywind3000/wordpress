---
uuid: 2589
title: 如何使用 C++ 写一个可编程软件渲染器？
status: publish
categories: 图形编程
tags: 图形
date: 2020-09-24 18:11
slug: 
---
今天你想用最新的 D3D12 画一个三角形，少说也要上千行代码了，对于初学者来讲，这个门槛是非常高的，太多干扰了，而一千多行代码，已经足够你重头实现一个简易版 D3D 了，为什么不呢？比起从图形 API 入门，不如从画点开始，同样一千行代码，却能让你对 GPU 的工作原理有一个直观的了解。

因此，为了让希望学习渲染的人更快入门，我开源了一个 C++ 实现可编程渲染管线的教程：

- [https://github.com/skywind3000/RenderHelp](https://github.com/skywind3000/RenderHelp)

那么网上软件渲染器其实不少，这个 RenderHelp 和他们有什么区别么？区别有三：

第一：实现精简，没依赖，就是一个 RenderHelp.h 文件，单独 include 它就能编译了，不用复杂的工程，导入一堆源文件，vim/vscode 里设置个 gcc 命令行，F9 编译单文件即可。

第二：模型标准，计算精确，网上很多软渲染器实现有很多大大小小的问题：比如纹理不是透视正确的，比如邻接三角形的边没有处理正确，比如 Edge Equation 其实没用对，比如完全没有裁剪，比如到屏幕坐标的计算有误差，应该以像素点方框的中心对齐，结果他们对齐到左上角去了，导致模型动起来三角形边缘会有跳变的感觉，太多问题了，对于强迫症，画错个点都是难接受的，RenderHelp 采用标准模型，不画错一个点，不算错一处坐标。

第三：可读性高，全中文注释，一千多行代码 1/3 是注释，网上很多同类项目，属于作者自己的习作，重在实现，做完了事，注释量不足 5%，一串矩阵套矩阵的操作过去，连行说明都没有，你想搜索下相关概念，连个关键字都不知道。RenderHelp.h 是面向可读性编写的，虽然也比较小巧，但重点计算全部展开，每一处计算都有解释。某些代码其实可以提到外层运行更快些，但为了可读性，还是写到了相关位置上，便于理解。

渲染效果图片：

![](https://skywind3000.github.io/images/p/renderhelp/model_4_s.jpg)

使用很简单，`include` 项目内的 `RenderHelp.h` 即可，VS 和 PS 之间传参，主要使用一个 `ShaderContext` 的结构体，里面都是一堆各种类型的 varying：

```cpp
// 着色器上下文，由 VS 设置，再由渲染器按像素逐点插值后，供 PS 读取
struct ShaderContext {
    std::map<int, float> varying_float;    // 浮点数 varying 列表
    std::map<int, Vec2f> varying_vec2f;    // 二维矢量 varying 列表
    std::map<int, Vec3f> varying_vec3f;    // 三维矢量 varying 列表
    std::map<int, Vec4f> varying_vec4f;    // 四维矢量 varying 列表
};
```

外层需要提供给渲染器 VS 的函数指针，并在渲染器的 DrawPrimitive 函数进行顶点初始化时对三角形的三个顶点依次调用：

```cpp
// 顶点着色器：因为是 C++ 编写，无需传递 attribute，传个 0-2 的顶点序号
// 着色器函数直接在外层根据序号读取响应数据即可，最后需要返回一个坐标 pos
// 各项 varying 设置到 output 里，由渲染器插值后传递给 PS 
typedef std::function<Vec4f(int index, ShaderContext &output)> VertexShader;
```

每次调用时，渲染器会依次将三个顶点的编号 0, 1, 2 通过 index 字段传递给 VS 程序，方便从外部读取顶点数据。

渲染器对三角形内每个需要填充的点调用像素着色器：

```cpp
// 像素着色器：输入 ShaderContext，需要返回 Vec4f 类型的颜色
// 三角形内每个点的 input 具体值会根据前面三个顶点的 output 插值得到
typedef std::function<Vec4f(ShaderContext &input)> PixelShader;
```

像素着色程序返回的颜色会被绘制到 Frame Buffer 的对应位置。

完整例子很简单，只需要下面几行代码就能工作了：（点击 Read more 展开）

<!--more-->

```cpp
#include "RenderHelp.h"

int main(void)
{
    // 初始化渲染器和帧缓存大小
    RenderHelp rh(800, 600);

    const int VARYING_COLOR = 0;    // 定义一个 varying 的 key

    // 顶点数据，由 VS 读取，如有多个三角形，可每次更新 vs_input 再绘制
    struct { Vec4f pos; Vec4f color; } vs_input[3] = {
        { {  0.0,  0.7, 0.90, 1}, {1, 0, 0, 1} },
        { { -0.6, -0.2, 0.01, 1}, {0, 1, 0, 1} },
        { { +0.6, -0.2, 0.01, 1}, {0, 0, 1, 1} },
    };

    // 顶点着色器，初始化 varying 并返回坐标，
    // 参数 index 是渲染器传入的顶点序号，范围 [0, 2] 用于读取顶点数据
    rh.SetVertexShader([&] (int index, ShaderContext& output) -> Vec4f {
            output.varying_vec4f[VARYING_COLOR] = vs_input[index].color;
            return vs_input[index].pos;        // 直接返回坐标
        });

    // 像素着色器，返回颜色
    rh.SetPixelShader([&] (ShaderContext& input) -> Vec4f {
            return input.varying_vec4f[VARYING_COLOR];
        });

    // 渲染并保存
    rh.DrawPrimitive();
    rh.SaveFile("output.bmp");

    return 0;
}
```

运行后，生成一张 `output.bmp` 图片：

![](https://skywind3000.github.io/images/p/renderhelp/sample_1.jpg)

由于 VS/PS 全部 C++ 编写，因此开发和调试都较方便，无需分开单独编译，能直接访问各种全局变量，能 printf 信息，还能断点观察问题。如果 Windows 的话，最后你可以加一行：

```cpp
system("mspaint output.bmp");
```

这样每次运行后就能打开画板程序查看最新的渲染效果。

有了上面绘制三角形的代码，我们可以继续改写载入个模型绘制下：

![](https://skywind3000.github.io/images/p/renderhelp/model_1_s.jpg)

直接显示模型纹理，光秃秃的太丑，加个高洛德着色：

![](https://skywind3000.github.io/images/p/renderhelp/model_2_s.jpg)

稍微能看一点，像十多年前的网游，再加个法向贴图，让细节更丰富些：

![](https://skywind3000.github.io/images/p/renderhelp/model_3_s.jpg)

看着还行，再加层高光：

![](https://skywind3000.github.io/images/p/renderhelp/model_4_s.jpg)

看起来不错，主要用于验证渲染器，有兴趣你可以继续折腾 PBR/BRDF 等高级渲染技巧。

渲染器的主要实现原理很简单，我在下面这篇文章介绍过：

- [OpenGL / DirectX 如何在知道顶点的情况下得到像素位置？](/blog/archives/2594)

两种光栅化的实现方式，基于 Edge Walking 和扫描线绘制的适合 CPU 的传统实时软渲染方法，和现在这个基于 Edge Equation 的适合 GPU 的方法。前者复杂但是速度快，适合 CPU 实时渲染；后者简单，但是运算量大，适合 GPU 并行处理。

欢迎参考我十多年前做的另外一个软件渲染器：

- [mini3d: 700 行 C 语言实现软件实时渲染](/blog/archives/1498)

走的是传统 CPU 实时渲染方法，其他参考：

- [计算机底层是如何访问显卡的？](/blog/archives/1774)
- [256字节3D程序是如何实现3D引擎的呢？](/blog/archives/2472)
- [3D 图形光栅化的透视校正问题](/blog/archives/1828)


