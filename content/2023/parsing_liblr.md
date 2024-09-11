---
uuid: 2671
title: 基于 LR(1) 和 LALR 的 Parser Generator
status: publish
categories: 编译原理
tags: 编译原理
date: 2023-01-26 11:47
slug: 
---
最近处理文本比较多，先前想增强下正则，看来不够用了，有同学推荐了我 Pyl 和 Lark，看了两眼，初看还行，但细看有一些不太喜欢的地方，于是刚好春节几天有空，从头写了一个 LR(1) / LALR 的 Generator，只有一个 LIBLR.py 的单文件，没有其它依赖：

- [GitHub - skywind3000/LIBLR: Parser Generator for LR(1) and LALR](https://github.com/skywind3000/LIBLR)

用法很简单，给定文法，返回 Parser：

```python
import LIBLR

# 注意这里是 r 字符串，方便后面写正则
# 所有词法规则用 @ 开头，从上到下依次匹配
grammar = r'''
start: WORD ',' WORD '!';

@ignore [ \r\n\t]*
@match WORD \w+
'''

parser = LIBLR.create_parser(grammar)
print(parser('Hello, World !'))
```

输出：

```text
Node(Symbol('start'), ['Hello', ',', 'World', '!'])
```

默认没有加 Semantic Action 的话，会返回一颗带注释的语法分析树（annotated parse-tree）。

支持语义动作（Semantic Action），可以在生成式中用 `{name}` 定义，对应 name 的方法会在回调中被调用：

```python
import LIBLR

# 注意这里是 r 字符串，方便后面写正则
grammar = r'''
# 事先声明终结符
%token number

E: E '+' T          {add}
 | E '-' T          {sub}
 | T                {get1}
 ;

T: T '*' F          {mul}
 | T '/' F          {div}
 | F                {get1}
 ;

F: number           {getint}
 | '(' E ')'        {get2}
 ;

# 忽略空白
@ignore [ \r\n\t]*
# 词法规则
@match number \d+
'''

# 定义语义动作：各个动作由类成员实现，每个方法的
# 第一个参数 rule 是对应的生成式
# 第二个参数 args 是各个部分的值，类似 yacc/bison 中的 $0-$N 
# args[1] 是生成式右边第一个符号的值，以此类推
# args[0] 是继承属性
class SemanticAction:
    def add (self, rule, args):
        return args[1] + args[3]
    def sub (self, rule, args):
        return args[1] - args[3]
    def mul (self, rule, args):
        return args[1] * args[3]
    def div (self, rule, args):
        return args[1] / args[3]
    def get1 (self, rule, args):
        return args[1]
    def get2 (self, rule, args):
        return args[2]
    def getint (self, rule, args):
        return int(args[1])

parser = LIBLR.create_parser(grammar, SemanticAction())
print(parser('1+2*3'))
```

输出：

（点击 more 查看更多）

<!--more-->

```text
7
```

Action 可以写在生成式右侧的任意位置，不象 Ply 和 Lark 那样只能写在最后，能用 args[0] 访问继承属性。之所以不像 Yacc 那样直接把代码贴到文法里，仅仅写个名字再由外层提供回调，是应为这样以后可以支持多种语言导出，不和会 Python 耦合太深，同时文法更干净点。

支持类似 Yacc/Bison 的基于优先级的冲突处理机制，来决定使用哪个规则，可书写二义文法：

```python
import LIBLR

# 注意这里是 r 字符串，方便后面写正则
grammar = r'''
%token NUMBER

%left '+' '-'
%left '*' '/' '%'
%right UMINUS

expr: expr '+' expr             {add}
    | expr '-' expr             {sub}
    | expr '*' expr             {mul}
    | expr '/' expr             {div}
    | '(' expr ')'              {get2}
    | '-' expr %prec UMINUS     {negative}
    | NUMBER                    {getint}
    ;

@ignore [ \r\n\t]*
@match NUMBER \d+
'''

class SemanticAction:
    def add (self, rule, args):
        return args[1] + args[3]
    def sub (self, rule, args):
        return args[1] - args[3]
    def mul (self, rule, args):
        return args[1] * args[3]
    def div (self, rule, args):
        return args[1] / args[3]
    def get1 (self, rule, args):
        return args[1]
    def get2 (self, rule, args):
        return args[2]
    def getint (self, rule, args):
        return int(args[1])
    # 注意，这里对应生成式 expr: '-' expr，因为前面有减号了
    # 所以右边 expr 的值对应的是 args[2]
    def negative (self, rule, args):
        return -(args[2])

parser = LIBLR.create_parser(grammar, SemanticAction())
print(parser('1+2*3+(5-2)*2'))
```

使用：`%left`, `%right`, `%noassoc` 同时定义优先级和结合方向，写在后面的终结符优先级更高。默认一个生成式的优先级由最右边的终结符优先级决定，也可以显式的用 `%prec` 指明。

对比前面的例子，使用二意文法，能让 BNF 的书写精简不少，该程序的输出：

```text
13
```

词法部分也可以自己定义非规则 Lexer，传一个 Token 的 list 或者 generator （可以 for 和 next 的那种 python 对象）到 parser 第一个参数即可。

基本上实现了 Yacc 的主要功能，

欢迎尝试。

