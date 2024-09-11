---
uuid: 2768
title: Emake：你见过最简单的 C/C++ 构建工具
status: publish
categories: 未分类
tags: 好用工具
slug: 
date: 2024-08-29 01:05
---
CMake 已经成为 C++ 构建工具事实上的标准了，即便觉得它很难用，但项目发布，跨部门协同，基本都以 cmake 为准。尽管你可能觉得其它构建工具更顺手，没问题，你们平时用就行，但项目发布或者跨团队协同时，你得同时用上 cmake 来标准化。

那么对于内部中小项目，非正式个人练手项目，或者非发布阶段的开发过程，是否也需要上 cmake 呢？还真不一定，一旦不用 cover 整个宇宙的构建需求，我们大可以找一个趁手的二号构建工具，满足平时使用。那么哪个二号构建工具值得推荐呢？

很多流行的构建工具，从 xmake 到 meson，恐怕都不适合，因为他们都试图同 cmake 去竞争试图要 cover 整个宇宙，即便号称精简，也不可能精简到哪里，尽管他们最简单的 demo 看起来好像真的超简单，但再稍微复杂点，比如考虑多平台架构，加个 release/debug 和包管理，一个个都变得丑陋不堪，立马原型毕露，因为他们都是命令式的。

我从 2009 年开发了一个叫做 emake 的构建工具，就是一个 emake.py 的单一脚本，持续使用并陆陆续续迭代了 15 年，今天感觉可以让他出来走两步。

推荐它，因为它有可能是你见过最简单的构建工具了，简单到什么程度呢？

（点击 more 展开阅读）

<!--more-->

#### 第一：定义式构建工具

简单点例子：main.mak 就三行：

```makefile
flag: -Wall, -O3
mode: exe
src: foo.c, bar.c, main.c
```

第一行设定编译参数，第二行指明目标格式，第三行设定源代码，这也是大部分时候写点小玩具，小测试的样子，然后：

```bash
emake main.mak
```

就能生成 `main.exe` 了，定义式的意思就是不像 `cmake` 一样每次要在 `CMakeLists.txt` 里写个小程序，而是跟 IDE 一样定义好源文件，设定好 release/debug 的编译参数，然后 emake 帮你做好默认工具链初始化，依赖分析，多核编译等等一堆琐事。

而且还没有 cmake 的 `rm -rf build && mkdir build && cmake -B build -G "MinGW Makefiles" .` 初始化环节，这个初始化每次都很蛋疼，极大的阻碍了我创建新项目的热情。更不用在 build 目录生成一大堆 shit，写好 emake 工程文件就能直接编译出可执行了，没有任何第二层构建工具的依赖。

也不会每个项目像 cmake 一样单独占用一个目录，我一堆小项目全部放一个目录里都没事情。到这里你可能会说，好像也没比 xmake 简单多少啊？别急我们还能继续简化。

#### 第二：零工程文件

如果你连工程文件都懒得写，没关系，emake 支持以 **docstring** 的形式将工程配置写到代码中：

```cpp
#include <stdio.h>

//! flag: -Wall, -O3
//! src: foo.c, bar.c
int main() {
    ...
}
```

这些以 //! 开头的注释可以用来描述项目配置，然后：

```bash
emake main.c
```

就能生成 main.exe 了，连工程文件都不需要，你把上述命令配置到 vscode / vim 里，按 F9 就能编译一个简单的项目，连 "mode: exe" 都不需要写，默认值即可，需要第三方库了就在加一行：

```cpp
//! link: zlib, m
```

就能链接对应的 `.a` 静态库了。

复杂的项目都是由一个个小的想法组成的，在写复杂项目之前，往往有大量的小的想法需要验证，小的模块需要开发，对于 “**编码-构建-测试**” 这个内循环，属于核心工作流，任何一个环节改进一点，都能带来极大的效率提升，这种 docstring 内嵌的方式，可以极大的简化你验证想法的成本。

还能降低你创建新项目的心理门槛，想建就建，你会发现你更容易开始一个新模块的开发了，等到模块变得足够复杂了，再将这些 docstring 独立出来，放到一个统一的工程文件里。

看到这里也许你会觉得是简化了一些，但 xmake 之类的对简单项目好像也不复杂啊？

别急，我们把需求稍微增加点，支持跨平台编译，支持区别 debug/release 区别就明显了。

#### 第三：条件编译

有个模块需要在 Windows / Linux 下运行，需要区别 debug/release 该怎么写？简单：

```makefile
src: src/main.c
win32/flag@release: -O3, -Wall
win32/flag@debug: -Og, -g
linux/define: TEST1, TEST2
```

分别在 Windows 平台的 debug/release 两种配置中定义了不同的 flag ，并在 linux 下面定义了两个宏（不区分 debug/release），编译时：

```bash
emake --profile=release main.mak    # 按照 release 模式编译
emake --profile=debug main.mak      # 按照 debug 模式编译
```

只有四行配置，搞定跨平台多模式构建。

横向对比下 xmake：

```lua
target("main")
    set_kind("binary")
    add_files("src/main.c")
    if is_plat("macosx", "linux") then
        add_defines("TEST1", "TEST2")
    end
    if is_plat("windows") then
        if is_mode("release") then
           add_cxflags("-O3")
        else
           add_cxflags("-Og")
        end
    end
```

号称简单的 xmake 立马不那么简单了，同样 cmake 也没好到哪里去：

```cmake
project(main)
add_executable(main 
    src/main.c
)
if (WIN32)
    set(CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG} -Og")
    set(CMAKE_C_FLAGS_RELEASE "${CMAKE_C_FLAGS_RELEASE} -O3")
endif()
if (LINUX)
    target_compile_definitions(main PRIVATE TEST1 TEST2)
endif()
```

对比下前面 emake 的 4 行工程文件，哪种更简单？你更想写哪种？需求稍微完善点，那些号称简单的构建工具们，一个个都原形毕露了。

#### 第四：第三方包引入

这个更简单：

```makefile
package: python3, sqlite3, curl
```

就行了，emake 会使用 `pkg-config` 将这几个包的 `.pc` 文件信息提取出来并分析他们的依赖图（比如会进一步补充 lzma, openssl 之类的 python3 依赖），然后添加到 `CFLAGS` 和 `LDFLAGS` 上去。

如果你的 /usr/lib/pkgconfig 下面没有对应 `.pc` ，比如你的第三方库随意乱放，没 install 时，当然也可以手工指定 include 目录，和静态库链接选项，但库多了会略显繁琐。

#### 第五：多套工具链切换

默认工具链配置位于 `~/.config/emake.ini` ，默认不提供的话 emake 能自动搜索 $PATH 里的工具，其它工具链位于 `~/.config/emake/{name}.ini` 使用时用 `--cfg={name}` 指明：

```bash
emake --cfg=mingw32-gcc12 <arguments>
```

就会读取 `~/.config/emake/mingw32-gcc12.ini` 的工具链配置进行初始化了，一般程序员机器上都会不止一套工具链，比开发 Windows 下 32/64 位的程序，或者交叉编译 android 平台等。

配置一个新的工具链很简单，只需要在 ini 文件里写入：

```ini
[default]

# 工具链的 bin 目录，用于查找 gcc / clang 等工具
home=d:/msys32/mingw32/bin

# 当你有多套工具链时，不可能都加入 $PATH，这个配置可以让 emake 在
# 构建时临时追加到 $PATH 前面，不污染外层父进程的环境变量
path=d:/msys32/mingw32/bin,d:/msys32/usr/bin

# 通用配置，免得每个工程文件写一遍
flag=-Wall
link=stdc++, winmm, wsock32, user32, ws2_32
cflag=-std=c11
cxxflag=-std=c++17

# 针对 debug/release/static 三种 profile 的设置，使用
# emake --profile=<name> xxx 在构建时指明使用啥 profile
define@debug=_DEBUG=1
define@release=_RELEASE=1
define@static=_STATIC=1, _RELEASE=1

flag@debug=-Og, -g, -fno-omit-frame-pointer
flag@release=-O3
flag@static=-O3, -static

# 多核编译
cpu=4

# 目标平台名称，不提供得话默认用 python 的 sys.platform 字符串代替
target=win32

# 条件编译时候的条件变量，在工程文件里可以用 win32/flag: xxx 来使用
name=win32,nt,have_openssl
```

其实不用写那么多，平时只要 `home` 和 `path` 两项定义好就行，后面的都是一些公共配置的演示，可以进一步帮助少写点工程文件。

写好多个 ini 文件放到 `~/.config/emake` 目录下面的话，就能随时切换多套工具链：

```bash
emake --cfg=mingw32-gcc12  project.mak     # 32 位 Windows 程序，GCC-12
emake --cfg=mingw64-gcc12  project.mak     # 64 位 Windows 程序，GCC-12
emake --cfg=mingw32-gcc53  project.mak     # 用 gcc-5.3 工具链构建 Windows XP 兼容程序。
emake --cfg=clang32  project.mak           # 使用 clang 构建
emake --cfg=android-16-arm  project.mak    # 交叉编译 Android 16 的 arm 程序
emake --cfg=android-16-x86  project.mak    # 交叉编译 Android 16 的 x86 程序
```

我机器上有一堆工具链，随时随地，想切就切。

这个 emake 我从 2009 年不断迭代使用至今，用它构建过最复杂的项目是 webrtc，是的，我没用 google 那套，并且跨平台支持 android/windows/iOS。

虽然我对外的项目都会写一个 `CMakeLists.txt`，但同一个项目内也会包含一个 emake 工程文件我自己开发时使用，新项目一开始就用，直到两个月后足够复杂了，项目快完成了，我再写一个 cmake 的工程文件准备发布。

平时我自己验证一些想法，写一些小模块，做些中小项目也都是用它，配置在 vim/vscode 里，一键编译，很趁手，也没一直开发，陆陆续续更新了很多年，感觉可以拿出来见见人了。

项目地址：

- [https://github.com/skywind3000/emake](https://github.com/skywind3000/emake)

限于篇幅，还有很多功能没法说完，比如：

- 如何同 vcpkg 联动，导入 vcpkg 包？
- 如何导出 `compile_commands.json` ，供其它工具使用？
- 如何使用 clang 等非 gcc 工具？
- 如何构建动态库和静态库，如何给动态库导出 MSVC 能用的 `.lib` 文件？
- 如何位单个源文件指定不同的编译参数？
- 如何添加汇编语言源文件？
- 如何在 Windows 项目中加入 `.RC` 资源文件？
- 之类的，欢迎参考项目文档。

最后说一句：我觉得 emake 的最大价值在于它放弃了追求全宇宙，在特定的需求范围内寻求最优解，是一个很趁手的二号构建工具。

