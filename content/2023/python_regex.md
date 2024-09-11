---
uuid: 2757
title: Python 中使用组合方式构建复杂正则
status: publish
categories: 编译原理
tags: 词法分析
slug: 
date: 2023-01-17 15:16
---
正则写复杂了很麻烦，难写难调试，只需要两个函数，就能用简单正则组合构建复杂正则：

比如输入一个字符串规则，可以使用 `{name}` 引用前面定义的规则：

```python
# rules definition
rules = r'''
    protocol = http|https
    login_name = [^:@\r\n\t ]+
    login_pass = [^@\r\n\t ]+
    login = {login_name}(:{login_pass})?
    host = [^:/@\r\n\t ]+
    port = \d+
    optional_port = (?:[:]{port})?
    path = /[^\r\n\t ]*
    url = {protocol}://({login}[@])?{host}{optional_port}{path}?
'''
```

然后调用 `regex_build` 函数，将上面的规则转换成一个字典并输出：

```python
# expand patterns in a dictionary
m = regex_build(rules, capture = True)

# list generated patterns
for k, v in m.items(): 
    print(k, '=', v)
```

结果：

```text
protocol = (?P<protocol>http|https)
login_name = (?P<login_name>[^:@\r\n\t ]+)
login_pass = (?P<login_pass>[^@\r\n\t ]+)
login = (?P<login>(?P<login_name>[^:@\r\n\t ]+)(:(?P<login_pass>[^@\r\n\t ]+))?)
host = (?P<host>[^:/@\r\n\t ]+)
port = (?P<port>\d+)
optional_port = (?P<optional_port>(?:[:](?P<port>\d+))?)
path = (?P<path>/[^\r\n\t ]*)
url = (?P<url>(?P<protocol>http|https)://((?P<login>(?P<login_name>[^:@\r\n\t ]+)(:(?P<login_pass>[^@\r\n\t ]+))?)[@])?(?P<host>[^:/@\r\n\t ]+)(?P<optional_port>(?:[:](?P<port>\d+))?)(?P<path>/[^\r\n\t ]*)?)
```

用手写直接写是很难写出这么复杂的正则的，写出来也很难调试，而组合方式构建正则的话，可以将小的简单正则提前测试好，要用的时候再组装起来，就不容易出错，上面就是组装替换后的结果。

下面用里面的 url 这个规则来匹配一下：

（点击 more 展开）

<!--more-->


```python
# 使用规则 "url" 进行匹配
pattern = m['url']
s = re.match(pattern, 'https://name:pass@www.baidu.com:8080/haha')

# 打印完整匹配结果
print('matched: "%s"'%s.group(0))
print()

# 打印分组匹配结果
for name in ('url', 'login_name', 'login_pass', 'host', 'port', 'path'):
    print('subgroup:', name, '=', s.group(name))
```

输出：

```text
match text with pattern "url"
matched: "https://name:pass@www.baidu.com:8080/haha"

subgroup: url = https://name:pass@www.baidu.com:8080/haha
subgroup: login_name = name
subgroup: login_pass = pass
subgroup: host = www.baidu.com
subgroup: port = 8080
subgroup: path = /haha
```

可以取完整结果，也可以按照规则名字，取得里面具体某个部件得匹配结果。

这下可以方便的写复杂正则表达式了。

再 Python 的正则表达式里 `{xxx}` 是用来表示长度的，里面都是数字，如果里面是变量名的话不会和原有规则冲突，因此这个写法是安全的。

实现代码：

```python
import re

# 将 pattern 里形如 {name} 的文本，用 macros 里的预定义规则替换
def regex_expand(macros, pattern, guarded = True):
    output = []
    pos = 0
    size = len(pattern)
    while pos < size:
        ch = pattern[pos]
        if ch == '\\':
            output.append(pattern[pos:pos + 2])
            pos += 2
            continue
        elif ch != '{':
            output.append(ch)
            pos += 1
            continue
        p2 = pattern.find('}', pos)
        if p2 < 0:
            output.append(ch)
            pos += 1
            continue
        p3 = p2 + 1
        name = pattern[pos + 1:p2].strip('\r\n\t ')
        if name == '':
            output.append(pattern[pos:p3])
            pos = p3
            continue
        elif name[0].isdigit():
            output.append(pattern[pos:p3])
            pos = p3
            continue
        elif ('<' in name) or ('>' in name):
            raise ValueError('invalid pattern name "%s"'%name)
        if name not in macros:
            raise ValueError('{%s} is undefined'%name)
        if guarded:
            output.append('(?:' + macros[name] + ')')
        else:
            output.append(macros[name])
        pos = p3
    return ''.join(output)

# 给定规则文本，构建规则字典
def regex_build(code, macros = None, capture = True):
    defined = {}
    if macros is not None:
        for k, v in macros.items():
            defined[k] = v
    line_num = 0
    for line in code.split('\n'):
        line_num += 1
        line = line.strip('\r\n\t ')
        if (not line) or line.startswith('#'):
            continue
        pos = line.find('=')
        if pos < 0:
            raise ValueError('%d: not a valid rule'%line_num)
        head = line[:pos].strip('\r\n\t ')
        body = line[pos + 1:].strip('\r\n\t ')
        if (not head):
            raise ValueError('%d: empty rule name'%line_num)
        elif head[0].isdigit():
            raise ValueError('%d: invalid rule name "%s"'%(line_num, head))
        elif ('<' in head) or ('>' in head):
            raise ValueError('%d: invalid rule name "%s"'%(line_num, head))
        try:
            pattern = regex_expand(defined, body, guarded = not capture)
        except ValueError as e:
            raise ValueError('%d: %s'%(line_num, str(e)))
        try:
            re.compile(pattern)
        except re.error:
            raise ValueError('%d: invalid pattern "%s"'%(line_num, pattern))
        if not capture:
            defined[head] = pattern
        else:
            defined[head] = '(?P<%s>%s)'%(head, pattern)
    return defined

# 定义一套组合规则
rules = r'''
    protocol = http|https
    login_name = [^:@\r\n\t ]+
    login_pass = [^@\r\n\t ]+
    login = {login_name}(:{login_pass})?
    host = [^:/@\r\n\t ]+
    port = \d+
    optional_port = (?:[:]{port})?
    path = /[^\r\n\t ]*
    url = {protocol}://({login}[@])?{host}{optional_port}{path}?
'''

# 将上面的规则展开成字典
m = regex_build(rules, capture = True)

# 输出字典内容
for k, v in m.items(): 
    print(k, '=', v)

print()

# 用最终规则 "url" 匹配文本
pattern = m['url']
s = re.match(pattern, 'https://name:pass@www.baidu.com:8080/haha')

# 打印完整匹配
print('matched: "%s"'%s.group(0))
print()

# 按名字打印分组匹配
for name in ('url', 'login_name', 'login_pass', 'host', 'port', 'path'):
    print('subgroup:', name, '=', s.group(name))
```

完事，主要逻辑 84 行代码。
