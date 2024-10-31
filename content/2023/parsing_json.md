---
uuid: 2677
title: 使用 LIBLR 解析带注释的 JSON
status: publish
categories: 编译原理
tags: 编译原理
date: 2023-01-27 16:39
slug: 
---
前文《[基于 LR(1) 和 LALR 的 Parser Generator](https://www.skywind.me/blog/archives/2671)》里介绍了春节期间开发的小玩具 [LIBLR](https://github.com/skywind3000/LIBLR) ，今天春节最后一天，用它跑一个小例子，解析带注释的 json 文件。由于 python 自带 json 库不支持带注释的 json 解析，而 vscode 里大量带注释的 json 没法解析，所以我们先写个文法，保存为 `json.txt`：

```pascal
# 定义两个终结符
%token NUMBER
%token STRING

start: value                {get1}
     ;

value: object               {get1}
     | array                {get1}
     | STRING               {get_string}
     | NUMBER               {get_number}
     | 'true'               {get_true}
     | 'false'              {get_false}
     | 'null'               {get_null}
     ;

array: '[' array_items ']'                  {get_array}
     ;

array_items: array_items ',' value          {list_many}
           | value                          {list_one}
           |                                {list_empty}
           ;

object: '{' object_items '}'                {get_object}
      ;

object_items: object_items ',' item_pair    {list_many}
            | item_pair                     {list_one}
            |                               {list_empty}
            ;

item_pair: STRING ':' value                 {item_pair}
         ;

# 词法：忽略空白
@ignore [ \r\n\t]*

# 词法：忽略注释
@ignore //.*

# 词法：匹配 NUMBER 和 STRING
@match NUMBER [+-]?\d+(\.\d*)?
@match STRING "(?:\\.|[^"\\])*"
```

有了文法，程序就很短了，50 多行足够：（点击 more 展开）

<!--more-->

```python
import sys
import pprint
import LIBLR

from LIBLR import cstring

class JsonAction:

    def get1 (self, rule, args):
        return args[1]

    def get_string (self, rule, args):
        return cstring.string_unquote(args[1])  # 将 "xxx" 的字符串去掉引号

    def get_number (self, rule, args):
        text = args[1]
        if text.isdigit():
            return int(text, 0)
        return float(text)

    def get_true (self, rule, args):
        return True

    def get_false (self, rule, args):
        return False

    def get_null (self, rule, args):
        return None

    def list_empty (self, rule, args):
        return []

    def list_one (self, rule, args):
        return [args[1]]

    def list_many (self, rule, args):
        return args[1] + [args[3]]

    def get_array (self, rule, args):
        return args[2]

    def item_pair (self, rule, args):
        name = cstring.string_unquote(args[1])    # 将 "xxx" 的字符串去掉引号
        value = args[3]
        return (name, value)

    def get_object (self, rule, args):
        obj = {}
        for k, v in args[2]:
            obj[k] = v
        return obj

parser = LIBLR.create_parser_from_file('grammar/json.txt',
                                       JsonAction(),
                                       algorithm = 'lalr')

text = open('sample/launch.json').read()
pprint.pprint(parser(text))
```

就是这么简单，大部分是在处理 json 的语义，写起来比 yacc/bison 流畅多了。其中 `'grammar/json.txt'` 就是上面的 json 文法文件，可以改成对应目录；而 `sample/launch.json` 的内容见：[这里](https://github.com/skywind3000/LIBLR/blob/master/sample/launch.json) ，就是我 vscode 里的一个配置。

好了，运行上面的程序，顺利转换成 Python 对象：

```python
{'configurations': [{'cwd': '${fileDirname}',
                     'env': {'PATH': 'D:\\dev\\mingw32\\bin;${env:Path}'},
                     'name': 'GDB Launch',
                     'request': 'launch',
                     'target': '${fileDirname}\\${fileBasenameNoExtension}.exe',
                     'type': 'gdb',
                     'valuesFormatting': 'parseText'},
                    {'console': 'externalTerminal',
                     'cwd': '${fileDirname}',
                     'justMyCode': True,
                     'name': 'Python: Current File',
                     'program': '${file}',
                     'request': 'launch',
                     'type': 'python'},
                    {'MIMode': 'gdb',
                     'args': ['1'],
                     'cwd': '${fileDirname}',
                     'environment': [{'name': 'PATH',
                                      'value': 'D:\\dev\\mingw32\\bin;${env:Path}'}],
                     'externalConsole': True,
                     'miDebuggerPath': 'd:\\dev\\mingw32\\bin\\gdb.exe',
                     'name': 'C/C++: debug active file',
                     'program': '${fileDirname}\\${fileBasenameNoExtension}.exe',
                     'request': 'launch',
                     'setupCommands': [{'description': 'Enable pretty-printing '
                                                       'for gdb',
                                        'ignoreFailures': False,
                                        'text': '-enable-pretty-printing'}],
                     'stopAtEntry': False,
                     'type': 'cppdbg'}],
 'version': '0.2.0'}
```

文法 + 源代码一共写了 100 行，完事，感觉比 Yacc/Bison 写起来顺畅不少。

相关阅读：

- [基于 LR(1) 和 LALR 的 Parser Generator](/blog/archives/2671)
- [56 行代码用 Python 实现一个 Flex/Lex](/blog/archives/2761)



--
