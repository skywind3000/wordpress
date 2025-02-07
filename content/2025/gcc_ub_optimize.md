---
uuid: 3184
title: GCC 利用未定义行为进行优化正确么？
status: publish
categories: 编程技术
tags: 计算机系统
slug: 
date: 2025-01-19 00:37
---
说实话，编译器是否该利用 Undefined Behavior 进行优化目前都还是一个争议话题，主要是 gcc 开了个坏头，不予余力的在默认参数下利用 UB 来优化，举个例子，C 语言里带符号整数溢出是未定义行为，编译器应该假设它实际上以某种方式定义了：

```c
int foo(unsigned char c) {
    int value = 2147483600;
    value += c;
    if (value < 2147483600) 
        bar();
    return value;
}
```

但利用这个 UB 进行优化的编译器会认为，既然 x 不会是负数，那么 value < 2147483600 就永远不会发生，所以整个 if 语句以及后面的 bar() 调用将可以被忽略，变成：

```c
int foo(unsigned char c) {
    int value = 2147483600;
    value += c;
    return value;
}
```

这其实是一种很危险的做法，因为 C 语言可以跨越各种 CPU 架构编程，当年标准定义时，CPU 架构的差异比今天还大，在处理上面这类问题时，即便在今天，不同的架构结果并不一定相同，比如有的平台用补码表示负数，所以溢出了就会变成 -2147483648，而碰到反码或者原码表示负数的架构下，溢出了可能就变成 0 或者其它，所以一些事情根本就没法具体定义，必须留给具体编译器具体平台去处理。

Undefined Behavior 并不是说代码这么写是错的，相反他们都是语法正确的代码，真是错的应该就编译错误了，而是标准留个编译器实现者以自由，不去做限制，让他们根据实际平台，根据自己实现情况自行选择实现方式，而某些编译器实现选择利用它来进行优化了，那么如果本来就想利用特定平台的特性完成某些特定功能时，所以这类代码将没法写了。

关于这个问题，有个 X 友说的很准确，这里贴下译文（原文贴后面）：

亲爱的 C 程序员们，既然你们似乎无法阅读关于你们编程语言的文档，让我为你们解释一下什么是未定义行为，更重要的是它不是什么。

引用 C 标准：

> 未定义行为：本国际标准未做任何强制要求的行为。（Undefined behavior: behavior for which this International Standard imposes no requirements）

这意味着标准并没有规定某些表达式该如何表现，编译器的创造者们可以自由选择他们想要的行为，例如：

- 使编译失败
- 删除有问题的表达式并继续编译
- 发送给你的前任一条“我想你了”的消息
- 将你的票投给一个 XX 主义政党
- 甚至定义该行为（以平台特定的方式或非特定方式）

即，编译器的职责是合理处理未定义行为的情况。**C 标准并没有对编译器作者提出挑战，这不是 “尽情发挥，给我惊喜”，它仅仅是对某些表达式没有施加限制**，因为给予编译器作者自由选择其解决方案是合情合理的，因为这可能依赖于平台。

未定义行为并不是关于“被禁止的表达式”，它仅仅是语法上正确的 C 代码，而 C 标准对此并不关心。

到目前为止，这一切都是合理的。

在处理未定义行为时，编译器作者有多种选择：

- 偏向一致的语义
- 偏向性能
- 偏向实现的简单性
- ...
  
正确的答案总是 “默认优先语义而非性能”。可以有破坏语义的优化，但这些优化应该通过适当的编译选项来启用，以便那些知道自己在做什么的人（或至少在继续破坏代码之前，编译器会得到明确的同意）使用。

（点击 more/continue 继续阅读）

<!--more-->

让编译器默认具有一致的语义不仅减少了各种开发人员（包括经验丰富的开发人员）引入的错误，还极大地改善了开发人员的用户体验，因为这样可以让他们更好地推理代码，毫无畏惧地进行重构，并且总体上不必时刻担心优化器会搞砸他们的代码。

至于 “但您必须支持多个平台” 的论点，如果 GCC 的开发者想要这样，他们就会让整数溢出在编译时的行为与运行时的行为相同。也就是说，如果在运行时是环绕运算，那么在编译时也是环绕运算。或者，他们可以简单地拒绝承诺任何特定的整数溢出策略，而只是不过度尝试优化涉及算术运算的表达式。

不幸的是，GCC 的开发者和他们的社区一样愚蠢，他们不仅没有合理地定义未定义行为，反而假装这一切都与禁止表达式有关，并默认启用他们那些让语义破裂的优化。“看，妈的，代码快了5%，却带来了 5% 的更多 bug，搞得全世界的基础设施和生产代码都乱了！”

至于他们在整数溢出问题上的选择有多愚蠢，我们会另行讨论，但这则推文的要点并不是某个具体优化的糟糕，而是 GCC 将 C标准中的未定义行为作为借口来搞砸自己编译器的整体方法，这真是让人难以置信——这是只有少数人才能理解的全面退化。

任何有不同看法的人都应该被视为愚蠢，应该被限制接触任何计算机，保持50米的安全距离。

原文：[https://x.com/effectfully/status/1876231418357092534](https://x.com/effectfully/status/1876231418357092534)

这里还有个 [原文长截图](https://skywind3000.github.io/images/blog/2025/exploit_ub.png)。

