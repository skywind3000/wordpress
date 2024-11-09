---
uuid: 2761
title: 56 行代码用 Python 实现一个 Flex/Lex
status: publish
categories: 编译原理
tags: 词法分析
slug: 
date: 2023-10-30 01:03
---
作为 Yacc/Bison 的好搭档 Lex/Flex 是一个很方便的工具，可以通过写几行规则就能生成一个新的词法分析器，大到给你的 parser 提供 token 流，小到解析一个配置文件，都很有帮助；而用 Python 实现一个支持自定义规则的类 Flex/Lex 词法分析器只需要短短 56 行代码，简单拷贝粘贴到你的代码里，让你的代码具备基于可定制规则的词法分析功能。

原理很简单，熟读 Python 文档的同学应该看过 [regex module](https://docs.python.org/3.11/library/re.html) 帮助页面最下面有段程序：

```python
def tokenize(code):
    keywords = {'IF', 'THEN', 'ENDIF', 'FOR', 'NEXT', 'GOSUB', 'RETURN'}
    token_specification = [
        ('NUMBER',   r'\d+(\.\d*)?'),  # Integer or decimal number
        ('ASSIGN',   r':='),           # Assignment operator
        ('END',      r';'),            # Statement terminator
        ('ID',       r'[A-Za-z]+'),    # Identifiers
        ('OP',       r'[+\-*/]'),      # Arithmetic operators
        ('NEWLINE',  r'\n'),           # Line endings
        ('SKIP',     r'[ \t]+'),       # Skip over spaces and tabs
        ('MISMATCH', r'.'),            # Any other character
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    line_start = 0
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if kind == 'NUMBER':
            value = float(value) if '.' in value else int(value)
        elif kind == 'ID' and value in keywords:
            kind = value
        elif kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected on line {line_num}')
        yield Token(kind, value, line_num, column)
```

上面这个官方文档里的程序，输入一段代码，返回 token 的：名称、原始文本、行号、列号 等。

它其实已经具备好三个重要功能了：1）规则自定义；2）由上往下匹配规则；3）使用生成器，逐步返回结果，而不是一次性处理好再返回，这个很重要，可以保证语法分析器边分析边指导词法分析器做一些精细化分析。

我们再它的基础上再修改一下，主要补充：

- 支持外部传入规则，而不是像上面那样写死的。
- 规则支持传入函数，这样可以根据结果进行二次判断。
- 更好的行和列信息统计，不依赖 NEWLINE 规则的存在。
- 支持 flex/lex 中的 “忽略”规则，比如忽略空格和换行，或者忽略注释。
- 支持在流末尾添加一个 EOF 符号，某些 parsing 技术需要输入流末尾插入一个名为 \$ 的结束符。

对文档中的简陋例子做完上面五项修改，我们即可得到一个通用的基于规则的词法分析器。

改写后代码很短，只有 56 行：

(点击 more 展开)

<!--more-->

```python
def tokenize(code, specs, eof = None):
    patterns = []
    definition = {}
    extended = {}
    if not specs:
        return None
    for index in range(len(specs)):
        spec = specs[index]
        name, pattern = spec[:2]
        pn = 'PATTERN%d'%index
        definition[pn] = name
        if len(spec) >= 3:
            extended[pn] = spec[2]
        patterns.append((pn, pattern))
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in patterns)
    line_starts = []
    pos = 0
    index = 0
    while 1:
        line_starts.append(pos)
        pos = code.find('\n', pos)
        if pos < 0:
            break
        pos += 1
    line_num = 0
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        start = mo.start()
        while line_num < len(line_starts) - 1:
            if line_starts[line_num + 1] > start:
                break
            line_num += 1
        line_start = line_starts[line_num]
        name = definition[kind]
        if name is None:
            continue
        if callable(name):
            if kind not in extended:
                obj = name(value)
            else:
                obj = name(value, extended[kind])
            name = None
            if isinstance(obj, list) or isinstance(obj, tuple):
                if len(obj) > 0: 
                    name = obj[0]
                if len(obj) > 1:
                    value = obj[1]
            else:
                name = obj
        yield (name, value, line_num + 1, start - line_start + 1)
    if eof is not None:
        line_start = line_starts[-1]
        endpos = len(code)
        yield (eof, '', len(line_starts), endpos - line_start + 1)
    return 0
```

测试一下，待分析代码如下：

```python
code = '''
    IF quantity THEN
        total := total + price * quantity;
        tax := price * 0.05;
    ENDIF;
'''
```

我们像 Flex 一样从上到下定义一下规则，部分规则需要引入代码判断，这里用了 `check_name` 函数：

```python
keywords = {'IF', 'THEN', 'ENDIF', 'FOR', 'NEXT', 'GOSUB', 'RETURN'}

def check_name(text):
    if text.upper() in keywords:
        return text.upper()
    return 'NAME'

rules = [
        (None,       r'[ \t]+'),       # Skip over spaces and tabs
        ('NUMBER',   r'\d+(\.\d*)?'),  # Integer or decimal number
        ('ASSIGN',   r':='),           # Assignment operator
        ('END',      r';'),            # Statement terminator
        (check_name, r'[A-Za-z]+'),    # Identifiers or keywords
        ('OP',       r'[+\-*/]'),      # Arithmetic operators
        ('NEWLINE',  r'\n'),           # Line endings
        ('MISMATCH', r'.'),            # Any other character
]
```

上面规则第一条左边是 None，意思是直接忽略空格和制表符，基本和编写 lex 规则差不多了。

最后使用 tokenize 函数，第一个参数传入代码，第二个是规则，第三个是否生成 EOF 填写 None 忽略：

```python
for token in tokenize(code, rules, None):
    print(token)
```

输出如下：

```python
('NEWLINE', '\n', 1, 1)
('IF', 'IF', 2, 5)
('NAME', 'quantity', 2, 8)
('THEN', 'THEN', 2, 17)
('NEWLINE', '\n', 2, 21)
('NAME', 'total', 3, 9)
('ASSIGN', ':=', 3, 15)
('NAME', 'total', 3, 18)
('OP', '+', 3, 24)
('NAME', 'price', 3, 26)
('OP', '*', 3, 32)
('NAME', 'quantity', 3, 34)
('END', ';', 3, 42)
('NEWLINE', '\n', 3, 43)
('NAME', 'tax', 4, 9)
('ASSIGN', ':=', 4, 13)
('NAME', 'price', 4, 16)
('OP', '*', 4, 22)
('NUMBER', '0.05', 4, 24)
('END', ';', 4, 28)
('NEWLINE', '\n', 4, 29)
('ENDIF', 'ENDIF', 5, 5)
('END', ';', 5, 10)
('NEWLINE', '\n', 5, 11)
```

上面是一个简单例子，我们来解析点复杂点的，一段 C 语言代码：

先设定规则的核心逻辑：

```python
keywords = {
    'auto', 'break', 'case', 'char', 'const', 'continue', 'default',
    'define', 'do', 'double', 'elif', 'else', 'endif', 'enum',
    'error', 'extern', 'float', 'for', 'goto', 'if', 'ifdef',
    'ifndef', 'include', 'inline', 'int', 'line', 'long', 'noalias',
    'pragma', 'register', 'restrict', 'return', 'short', 'signed',
    'sizeof', 'static', 'struct', 'switch', 'typedef', 'undef',
    'union', 'unsigned', 'void', 'volatile', 'while', }

operators = (
    '++', '--', '.', '->', '~', '!=', '+=', '-=', '&&', '_Alignof',
    'sizeof', '?:', ',', '*=', '/=', '%=', '<<=', '>>=', '<=', '>=', 
    '<<', '>>', '==', '!', '||', '&=', '|=', '^=', '*', '/', '%',
    '+', '-', '>', '<', '&', '=', '|', '?', ':', '^', )

specials = {'(', '[', '{', '}', ']', ')', '#'}

def check_name(text):
    if text in keywords:
        return text
    if text in operators:
        return 'OP'
    return 'NAME'
```

然后定义规则的匹配方式：

```python
# patterns
PATTERN_WHITESPACE = r'[ \t\r\n]+'
PATTERN_COMMENT1 = r'\/\/.*'
PATTERN_COMMENT2 = r'\/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+\/'
PATTERN_NAME = r'\w+'
PATTERN_STRING1 = r"'(?:\\.|[^'\\])*'"
PATTERN_STRING2 = r'"(?:\\.|[^"\\])*"'
PATTERN_NUMBER = r'\d+(\.\d*)?'
PATTERN_CINTEGER = r'(0x)?\d+[uUlLbB]*'
PATTERN_MISMATCH = r'.'

rules = [
        (None, PATTERN_WHITESPACE),
        (None, PATTERN_COMMENT1),
        (None, PATTERN_COMMENT2),
        ('STRING', PATTERN_STRING1),
        ('STRING', PATTERN_STRING2),
        ('INTEGER', PATTERN_CINTEGER),
        ('NUMBER', PATTERN_NUMBER),
        (check_name, PATTERN_NAME),
        ('SEMICOLON', ';'),
]
```

最后对 rules 进行必要的扩充：

```python
# 注意：operators 是一个 list，按顺序添加，可以保证 ++ 的匹配优先级高于 +
for op in operators:  
    rules.append(('OP', re.escape(op)))

for sp in specials:
    rules.append((sp, re.escape(sp)))

rules.append(('MISMATCH', PATTERN_MISMATCH))
```

好了，可以用了，给一段 C 代码：

```python
code = '''
// My first C program
int main(void)
{
    int x = 10;
    int y = x+++3;
    printf("Hello, World !!\n");
    return 0;
}
'''

for token in tokenize(code, rules, None):
    print(token)
```

运行输出 token：

```python
('int', 'int', 3, 1)
('NAME', 'main', 3, 5)
('(', '(', 3, 9)
('void', 'void', 3, 10)
(')', ')', 3, 14)
('{', '{', 4, 1)
('int', 'int', 5, 5)
('NAME', 'x', 5, 9)
('OP', '=', 5, 11)
('INTEGER', '10', 5, 13)
('SEMICOLON', ';', 5, 15)
('int', 'int', 6, 5)
('NAME', 'y', 6, 9)
('OP', '=', 6, 11)
('NAME', 'x', 6, 13)
('OP', '++', 6, 14)
('OP', '+', 6, 16)
('INTEGER', '3', 6, 17)
('SEMICOLON', ';', 6, 18)
('NAME', 'printf', 7, 5)
('(', '(', 7, 11)
('STRING', '"Hello, World !!\n"', 7, 12)
(')', ')', 8, 2)
('SEMICOLON', ';', 8, 3)
('return', 'return', 9, 5)
('INTEGER', '0', 9, 12)
('SEMICOLON', ';', 9, 13)
('}', '}', 10, 1)
```

输出符合预期，你如果觉得编写那些 PATTERN_ 开头的正则规则比较困难，可以使用《[组合方式构建复杂正则](/blog/archives/2757)》的文章里的方法，三两下也就定义出来了。

你如果代码里有一些简单的词法分析需求，把上面这个 56 行的函数拷贝过去就够了，真的不必引入什么其他的复杂依赖。

<br>
<br>

\-\-

<br>

更多阅读：

- [LIBLR - 使用 Python 实现基于 LR(1) 和 LALR 的 Parser Generator](/blog/archives/2671)
- [使用 LIBLR 解析带注释的 JSON](/blog/archives/2677)


<br>

