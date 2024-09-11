---
uuid: 2656
title: 最近都流行实现 Coroutine 么 ？
status: publish
categories: 编程技术
tags: 汇编
slug: 
date: 2019-08-10 13:06
---
这两天看着大家都在实现无栈的 coroutine 都挺好玩的，但无栈协程限制太多，工程实践上很少用，所以昨天手痒写了个有栈的 coroutine ，接口反照 ucontext 的接口，不比无栈的复杂多少：

```c
int main(void)
{
	ctx_context_t r;
	int hr;
	volatile int mode = 0;

	hr = ctx_getcontext(&r);
	printf("ctx_getcontext() -> %d\n", hr);

	if (mode == 0) {
		mode++;
		printf("first run\n");
		ctx_setcontext(&r);
	}
	else {
		printf("second run\n");
	}
	printf("endup\n");

	return 0;
}
```

使用 ctx_getcontext / ctx_setcontext 可以实现保存现场，恢复现场的功能，该程序输出：

```bash
ctx_getcontext() -> 0
first run
ctx_getcontext() -> 6356604
second run
endup
```

继续使用 ctx_makecontext / ctx_swapcontext 可以实现初始化协程和切换上下文的功能：

```c
char temp_stack[32768];
ctx_context_t mc, cc;

int raw_thread(void*p) {
	printf("remote: hello %s\n", (char*)p);
	ctx_swapcontext(&cc, &mc);

	printf("remote: back again\n");
	ctx_swapcontext(&cc, &mc);

	printf("remote: return\n");
	return 1024;
}

int main(void)
{
	cc.stack = temp_stack;
	cc.stack_size = sizeof(temp_stack);
	cc.link = &mc;

	ctx_getcontext(&cc);
	ctx_makecontext(&cc, raw_thread, (char*)"girl");

	printf("before switch: %d\n", cc.stack_size);
	ctx_swapcontext(&mc, &cc);

	printf("local: here\n");
	ctx_swapcontext(&mc, &cc);

	printf("local: again\n");
	ctx_swapcontext(&mc, &cc);

	printf("local: end\n");
	return 0;
}
```

这里创建了一个协程，接着主程序和协程互相切换，程序输出：

```bash
before switch: 32768
remote: hello girl
local: here
remote: back again
local: again
remote: return
local: end
```

#### 关于实现

核心代码其实很简单，就 60 多行，没啥复杂的：

（点击 Read more 展开）

<!--more-->

```c
asm("\
.globl _ctx_swapcontext \n\
.globl ctx_swapcontext \n\
_ctx_swapcontext: \n\
ctx_swapcontext: \n"
#if CTX_OS_WINDOWS || __CYGWIN__
	"movq %rcx, %rax; \n"
#else
	"movq %rdi, %rax; \n"
#endif
	"\n\
	movq %rdx, 24(%rax); \n\
	movq %rax, 0(%rax); \n\
	movq %rbx, 8(%rax); \n\
	movq %rcx, 16(%rax); \n\
	movq %rsi, 32(%rax); \n\
	movq %rdi, 40(%rax); \n\
	leaq 8(%rsp), %rdx; \n\
	movq %rdx, 48(%rax); \n\
	movq %rbp, 56(%rax); \n\
	movq 0(%rsp), %rdx; \n\
	movq %rdx, 64(%rax); \n\
	pushfq; \n\
	popq %rdx;  \n\
	movq %rdx, 72(%rax); \n\
	movq %r8, 80(%rax); \n\
	movq %r9, 88(%rax); \n\
	movq %r10, 96(%rax); \n\
	movq %r11, 104(%rax); \n\
	movq %r12, 112(%rax); \n\
	movq %r13, 120(%rax); \n\
	movq %r14, 128(%rax); \n\
	movq %r15, 136(%rax); \n\
	movq 24(%rax), %rdx; \n\
	stmxcsr 144(%rax); \n\
	fnstenv 152(%rax); \n\
	fldenv 152(%rax); \n"
#if CTX_OS_WINDOWS || __CYGWIN__
	"movq %rdx, %rax\n"
#else
	"movq %rsi, %rax\n"
#endif
	"\n\
	movq 8(%rax), %rbx; \n\
	movq 16(%rax), %rcx; \n\
	movq 24(%rax), %rdx; \n\
	movq 32(%rax), %rsi; \n\
	movq 40(%rax), %rdi; \n\
	movq 48(%rax), %rsp; \n\
	movq 56(%rax), %rbp; \n\
	movq 64(%rax), %rdx; \n\
	pushq %rdx; \n\
	movq 72(%rax), %rdx; \n\
	pushq %rdx; \n\
	popfq; \n\
	movq 80(%rax), %r8; \n\
	movq 88(%rax), %r9; \n\
	movq 96(%rax), %r10; \n\
	movq 104(%rax), %r11; \n\
	movq 112(%rax), %r12; \n\
	movq 120(%rax), %r13; \n\
	movq 128(%rax), %r14; \n\
	movq 136(%rax), %r15; \n\
	movq 24(%rax), %rdx; \n\
	ldmxcsr 144(%rax); \n\
	fldenv 152(%rax); \n\
	movq 0(%rax), %rax; \n\
	ret; \n\
");
```

就是保存寄存器，保存栈，恢复寄存器，恢复栈，返回就得了，注意额外保存一下浮点数状态，SSE 控制寄存器状态，和 eflag / rflag 即可。

构造协程就是把一个新的栈和寄存器初始化好，需要注意的是 calling convention：

- [x86 calling conventions](https://en.wikipedia.org/wiki/X86_calling_conventions)

32位下面还好，Linux / Windows 都是可以用统一的 cdecl 约定，`4(%esp)` 代表第一个参数，`8(%esp)` 第二个参数，如此类推；64 位稍微有点烦，Linux / BSD / OS X / Solaris 都统一使用 **System V AMD64 ABI** 而微软一如既往的自己发明了一套只能用于 Windows 的 **Microsoft x64 calling convention**，给所有人添堵。

所以在切换上下文时和构造协程环境的时候需要额外注意一下，除此以外 300行也就搞定了：

- https://github.com/skywind3000/collection/tree/master/vintage/context

用 ctx_makecontext / ctx_swapcontext 分分钟可以包装出一个 yield，具体包装方法可以见云风的 [cloudwu/coroutine](https://github.com/cloudwu/coroutine) 项目。

接着封装下 epoll / socket ，加入些调度逻辑，你基本上就得到个腾讯的 libco 了。

#### 栈内存开销

一般有栈的协程主要问题是费内存，每个协程如果使用独立的栈的话，一开始创建过小，程序容易崩溃，特别是64位下面，一个函数调用的 frame 动辄几百字节的占用，你栈开小了就容易崩溃，栈这东西需要协程一开始就把地址确定下来，所以还不能用变长数组来保存，而你初始化很大的栈（比如每个协程1MB），又太费内存了，3000个协程就费 3G的内存，问题3000个协程是很正常的事情。

所以云风的 coroutine 和腾讯的 libco 的解决方法是 “栈拷贝”，初始化一个 4-8MB 的共有栈，每个协程都在这个共有栈上执行，只是进入和退出的时候需要把数据从共有栈备份/恢复到协程自己的变长数组里面，这样解决了空间浪费问题，也保证了协程的栈不会变来变去，但是带来了一个新问题，就是频繁切换时内存拷贝的开销。

#### 协程栈优化

所以其实他们都可以再优化一下，引入 stack 分组，初始化比如 100个栈，每个2MB ，协程初始化时选择一组负担轻的组加入进去，同组内的协程公用一个栈。

每个协程的栈有两个状态：ON_STACK / OFF_STACK，表示当前协程的栈是否就在这一组的公有栈上。协程 suspend 的时候，不必马上把栈拷贝回去，可以一直占用着该组的共有栈，直到有新协程恢复的时候，发现该组的共有栈上有一个 ON_STACK 的协程占用了，这时候再把它给踢走。

这样 100个栈上，基本都是被最活跃的几个协程所占用，且来切去很少发生拷贝栈的工作，整个栈拷贝开销基本都能下降 10-100 倍，如此有栈协程的内存开销问题得到解决，并消除了 所引入的副作用。

#### C/C++ 的协程好用么？

不过啊，协程着东西，我并不主张直接在 C/C++层次上使用，协程的目的是方便业务开发，降低业务逻辑的复杂度。是否需要在 C/C++ 上做协程，唯一的问题就是你是否需要把所有逻辑用 C/C++来实现？

其实如果你只是为了业务简单这个目的，你该直接去用 go / erlang / gevent / akka，这些封装成熟的库，出点问题调试起来信息也比较丰富，C/C++这种系统级语言本来就不适合写业务逻辑，除去开发效率外，协程出点问题，调试起来你是比较头疼的。

再者，如果不开发业务，而是开发系统级模块，那更应该直接手写状态机，因为系统级开发的 KPI是可靠和高效，并不是开发时间和复杂度。

所以 C/C++ 级别的协程，除非你给某个语言用 C/C++实现一套协程接口，或者自己觉得好玩写了娱乐一下，除此之外，写具体业务想上协程的话，C/C++的协程还是靠边站吧，建议大家直接使用 go / erlang / asyncio / akka。

