---
uuid: 2449
title: C语言如何编译出一个不需要操作系统的程序
status: publish
categories: 编程技术
tags: C++,系统开发
date: 2018-01-03 21:18
slug: 
---
来个更短的，没有其他乱七八糟的东西，只有一个简短的 C文件，不需要 linux 环境：

miniboot.c

```cpp
asm(".long 0x1badb002, 0, (-(0x1badb002 + 0))");

unsigned char *videobuf = (unsigned char*)0xb8000;
const char *str = "Hello, World !! ";

int start_entry(void)
{
	int i;
	for (i = 0; str[i]; i++) {
		videobuf[i * 2 + 0] = str[i];
		videobuf[i * 2 + 1] = 0x17;
	}
	for (; i < 80 * 25; i++) {
		videobuf[i * 2 + 0] = ' ';
		videobuf[i * 2 + 1] = 0x17;
	}
	while (1) { }
	return 0;
}
```

编译：

```bash
gcc -c -fno-builtin -ffreestanding -nostdlib -m32 miniboot.c -o miniboot.o
ld -e start_entry -m elf_i386 -Ttext-seg=0x100000 miniboot.o -o miniboot.elf
```

运行：

```bash
qemu-system-i386 -kernel miniboot.elf
```

结果：

![](http://skywind3000.github.io/word/images/assets/qemu-1.jpg)

满足条件：

- 只用纯 C 开发，可以使用 gcc 编译
- 编译出来的东西真的可以运行
- 不需要依赖操作系统
- 不需要包含系统调用的 glibc
- 连 libgcc 都不需要

解释一下：

<!--more-->
**Q：-m elf_i386 是什么鬼？为何使用 elf 格式？**

是输出为 elf 的目标格式，386是目标平台，还可以输出成 binary 格式，就是没有任何额外信息，你代码里面写了什么就是什么。一般用在 boot loader stage1 的第一个 512字节扇区那里，就是用这种纯格式。

但是这里我们需要 elf 格式，因为 elf格式除了代码和数据外还有很多有用的信息，可以被标准 boot loader 识别，你如果不想自己花费10+天去自己实现 stage1 和 stage2 的 bootloader 的话，elf文件可以帮你省很多时间，因为 grub 可以直接加载，qemu 也可以直接运行。

**Q：elf 包含了哪些内容？**

代码段，数据段的运行位置（比如你有个全局变量，需要知道到哪个线性地址可以找到这个全局变量），各个段的线性地址从低到高的排列顺序，以及他们的加载地址，加载地址和运行地址可以不同，加载地址是告诉 boot loader 把这个段加载到哪里，比如加载地址可以是0x100000即1MB地址开始处，也是最常见做法，而运行地址可以是 0xc0000000 即最高端内存 1GB 的位置，还有程序入口的起始地址，最后还可以包含符号信息便于调试。这些丰富的信息可以告诉外层的 boot loader 如何加载我们的 elf 文件，到哪里去初始化我们的 bss 数据段，以及最终跳转到哪里去执行入口处的代码，这些内存布局信息需要再一个 .ld 文件里说明，这里我们不用 .ld 文件，全部使用默认配置，但后期你想详细指定这些的话，需要写 .ld 文件，链接的时候传递给 ld 程序。

**Q：是不是所有 elf 文件都可以被 boot loader 加载？**

不是，需要第一个段中（没有ld文件的话，第一个段默认就是 text）头部包含 multiboot header，就是：

```cpp
asm(".long 0x1badb002, 0, (-(0x1badb002 + 0))"); 
```

一共定义了十二个字节的 multiboot header，第一个long是 magic code, grub/qemu等需要检查，第二个 long 代表你需要 grub 提供哪些信息（比如内存布局，elf结构），这里填写0，不需要它提供任何信息。第三个long是代表前两个运算以后的一个 checksum，grub/qemu 会检查这个值确认你真的是一个可以引导的 kernel。

**Q：为什么加载到 0x100000 地址？**

这是最常规的做法，因为如果低于 1MB的地址你可能会破坏到 BIOS 程序，显存，中断引射表，而且低端地址需要保留给 dma 使用。而如果加载到，比如 0x800000，也不是不可以，只是你需要保证目标电脑内存 \> 8MB + 你的程序大小，所以 0x100000 这个地址是大家都可以接受的一个通用地址。

**Q：我想再高端内存（0xc0000000）运行？**

可以，这也是 linux 干的事情，这样可以给下面的应用程序留出足够的线性空间来，但是你需要初始化页表，把你自己映射到高端地址，并且需要再 .ld 文件里面指明加载地址（0x100000处）和运行地址（0xc0000000）是两个不同的地址，你还是会被加载到 0x100000 处，但是你的所有C代码都认为自己再 0xc0000000 处执行，所以此时还不能跑任何C代码，需要一段叫做 relocation 的汇编初始化页面映射，还有其他一些环境，并最终跳转到高端地址的 entry 入口。

**Q：为什么不写 boot loader ?**

给你节省时间，完善的boot loader涉及到大量的技巧，用现成的boot loader，可以让你马上看到结果，有正反馈。

**Q：如果我执意要写个完善的 boot loader 呢？**

首先要写引导扇区代码，调用 BIOS 磁盘中断，把你后面的 elf 文件加载进来，但是这时boot loader还处在实模式，只能访问 1MB以内的空间，也就是说你的 elf 文件大小受到了限制，要加载到 1MB以上的空间，需要 boot loader 切换到保护模式，但是此时又不能访问传统的 BIOS 中断请求磁盘了，所有你需要来回切换保护模式和实模式，或者用 v86 模式，或者写保护模式下的硬盘驱动，显然这不是 512字节能够完成的事情，所以你还需要 stage 2 的 boot loader。

传统 512 字节的 boot loader 先在实模式下把 stage 2 加载到 0x10000 处（64KB处），然后又由 stage2 的程序进入保护模式，并用 v86 模式调用 BIOS 的磁盘中断服务程序，把你的 elf 文件找出来，并且解析 elf 结构，把各个段加载到它期望的位置，最后初始化一个临时的 GDT 和栈，把 bss 段全部置0，关闭中断标志，最后再跳转到 elf 的 entry 处，完成引导。

注意：stage1 的 512字节，和 stage2的后续扇区代码，目标格式都是纯二进制，不是 elf。

注意：stage2 的代码里需要找出你的 elf，这时你的 elf 可以简单的写到一个裸分区上，这样找起来容易点，如果你需要把 elf 放到 fat16/fat32 分区的某个目录中，那么 stage2 代码就要写相关 fat 文件系统的识别代码（只需要简单的文件/目录读取，不需要写，所以不需要实现整个文件系统），而如果你想把 elf 文件放到除 fat 外的其他文件系统需要支持多文件系统的话，stage2就搞不定了，需要 stage3 可以动态加载不同文件系统的模块化程序，做更复杂的动作。

**Q：这个 miniboot 程序可以接着自由往下写么？**

很遗憾，可能你只能写点很短的代码，因为：

1. 你还没有relocate，一直在1MB处跑你的代码不是件好事，尽早重定位到最高1GB处。
1. 你还没有初始化栈，你不知道 grub 到底给你的栈指针 esp 设定到哪里了，你需要自己规划栈空间。
1. 你没有 libc 库，什么 memcpy, strlen , printf 都没有，你需要一个个实现。
1. 你没有 libgcc 库（是gcc的一部分），可能你做64为乘除法的代码无法得到链接，或者你在类似 arm 的平台下连 32为的除法都没法做，在 risc v 的标准平台下，连普通乘法都没有，一旦写了链接就不通过，因为没有 libgcc，你可以软件模拟（控制狂的话），或者选择链接 libgcc。
1. 硬件你还没探测，最基本的，你都还不知道你的内存多大，怎么布局的（根据接口不同，内存各个模块的物理地址不一定连续）。
1. 你没法接受键盘输入，需要初始化键盘中断来接管键盘。
1. 你没有办法读取磁盘，因为你现在是保护模式，BIOS 下面的磁盘访问程序都是实模式的，幸好你加载到1MB地区没覆盖他们，这时候你可以用v86模式去调用这些中断，或者自己写硬盘驱动。
1. 你还没有相关调试手段，往下写出点错误可能都会折腾死你，backtrace 要有吧，panic要有吧，最好能搜索符号表把函数名都打印出来，最好初始化串口，用com1 和外部通信，这样比把信息输出到屏幕靠谱，屏幕大小有限，信息稍纵即逝，com1的话可以和外部串口中端进行通信，qemu/bochs还可以把com1的内容记录到日志文件，永久保存。
1. 你还没法分配内存，你需要把前面内存探测结果里的可用物理内存页面统计起来，先实现基于页面的分配和映射，再以前面为基础实现基于对象的分配，然后你才有 malloc / free。

先把这九个问题解决，你就可以继续往下写更多复杂的内容了。



先写这么多吧。
