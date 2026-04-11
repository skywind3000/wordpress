# AGENTS.md

本仓库是个人文档的仓库，所有 agent 活动前请先阅读并遵守本文档：

## Description

目录结构如下：

```
- content    # 文章内容主目录，内部安年份分类，含所有文章
- legacy     # 旧文章（归档，不会再更新）
- extra      # 辅助资料
- script     # 辅助脚本
- scratch    # 临时目录，不会被提交到 git 等地方；
```

所有文章都以 `content` 目录为准，目录 `legacy` 只是一些归档的文档。如果存在同个 uuid 的文章同时出现在 `content` 和 `legacy`，哪怕文件名不同，他们都是相同的文章，并且内容以 `content` 的为准。

### Meta Information

每篇文章都是一个 `.md` 的 Markdown 文件，他有统一的头部，以 3+ 个连续的 `-` 为分割：

```
---
uuid: 3671
title: 使用 rclone bisync 两步搭建个人云盘
status: publish
categories: 随笔
tags: Linux,网络
slug: 
date: 2026-01-30 00:27
---
Markdown body
```

里面的字段占一行，由 `:` 符号分割，左边是名称，右边是值，其中最重要的是 `uuid` 即文章的唯一编号，这是一个整数；

## 解析代码

解析上面说到的头部元信息的 Python 代码如下：

```python
def extract_meta_information (content: str):
    state = 0
    meta = {}
    size = len(content)
    pos = 0
    while pos < size:
        end = content.find('\n', pos)
        if end < 0:
            end = size
        line = content[pos:end]
        pos = end + 1
        line = line.rstrip('\r\n\t ')
        if not line:
            continue
        if state == 0:
            if line == ('-' * len(line)) and len(line) >= 3:
                state = 1
            else:
                break
        elif state == 1:
            if line == ('-' * len(line)) and len(line) >= 3:
                state = 2
            elif ':' in line:
                key, _, value = line.partition(':')
                key = key.strip()
                if key:
                    meta[key] = value.strip()
        else:
            break
    return meta
```

把包含这种头部的 Markdown 文本传进去，就能将头部的元信息提取出来；

## Guidelines

- 所有生成的脚本，长期反复使用的，默认放在 `script` 目录下；
- 而如果是一次性测试的脚本，放到 `scratch` 下；