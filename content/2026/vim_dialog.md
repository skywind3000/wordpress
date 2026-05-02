---
uuid: 3676
title: 在 Vim 里实现可定制表单对话框
status: publish
categories: 随笔
tags: Vim
slug: 
date: 2026-05-02 20:25
---

![](https://skywind3000.github.io/images/p/quickui/dialog1.gif)

Vim 的功能非常强大，但这种强大是有代价的——你得把它全部**记住**。

## 记忆的负担

就拿替换命令来说。"查找替换"这么一个最常见的编辑操作，在 Vim 里有一堆变体：

- 替换所有匹配项，而不只是每行第一个？加 `g`。
- 每次替换前要确认？加 `c`。
- 不区分大小写？加 `i`。或者在模式里写 `\c`。
- 要不要用正则？默认就是正则。但用哪种风格？`\v` 是 very-magic，`\V` 是纯文本，还有默认的 magic 模式，各有各的转义规则。
- 只匹配整个单词？用 `\<` 和 `\>` 把模式包起来。容易忘，也容易打错。
- 替换整个文件？前面加 `%`。只替换选中区域？用 `'<,'>`。指定行范围？输入行号。

于是你写出这样的命令：

```vim
:%s/\v(foo|bar)/baz/gci
```

新手要花很久才能记住这些标志位。有经验的用户也会忘掉不常用的那几个。

而且替换只是一个内置命令。真正麻烦的是插件——每个插件都有自己的命令、自己的参数和语法。天天用的那些还好，肌肉记忆自然形成；但那些偶尔才用一次的？每次都得重新翻文档。

这就是 Vim 界面的根本矛盾：命令行天生为**速度**优化，而不是为**可发现性**优化。如果你已经记住了命令，它快得飞起；如果你忘了——哪怕只是忘了一个标志位——就只能干瞪眼。

如果能把一个命令的所有可选项一次性展示在用户面前呢？不是藏在 `:help` 里，而是就在屏幕上，一目了然：

![](https://skywind3000.github.io/images/p/quickui/dialog6.gif)

这是一个用 [vim-quickui](https://github.com/skywind3000/vim-quickui) 搭建的查找替换对话框。所有选项清清楚楚：正则模式、大小写敏感、全词匹配、是否确认、替换范围。不管是第一次用，还是隔了几个月再回来用，完全没有记忆负担——你看到有什么选项，勾选你需要的，直接开始。

<!--more-->

那么问题来了，在 Vim 里怎么才能做出这样的对话框？

原生工具帮不了你太多。Vim 给你的只有 `input()` 做单行输入和 `inputlist()` 做简单列表选择——没有文本框，没有复选框，没有单选按钮，没有办法把多个控件放在一个窗口里。如果要做一个多字段的表单，只能一个接一个地调用阻塞式的 `input()`，而且填错了前面的内容没法回头修改。

**这种方式，不能扩展。**

## 更好的方式：vim-quickui Dialog

[vim-quickui](https://github.com/skywind3000/vim-quickui) 是一个为 Vim 和 NeoVim 设计的 TUI 组件库，提供菜单、列表框、文本框等控件——全部用纯 VimScript 实现，不依赖任何外部工具。

在 1.5.0 版本中，它新增了一套**数据驱动的对话框系统**：你把控件声明为一组字典，quickui 将它们渲染到一个弹出窗口中；用户完成操作后，所有值以一个字典返回给你。

不需要 `+python`，不需要 Lua，不需要外部依赖，纯 VimScript 搞定。

![](https://skywind3000.github.io/images/p/quickui/dialog4.gif)

对新手来说，这降低了上手 Vim 的门槛——不用先把每个命令和标志位都背下来，才敢去用一个功能。对老手来说，这减少了为偶尔使用的命令反复查文档的次数，让你保持在心流状态里。



## 安装

用 [vim-plug](https://github.com/junegunn/vim-plug)：

```vim
Plug 'skywind3000/vim-quickui'
```

或者用 Vim 内置包管理：

```bash
cd ~/.vim/pack/vendor/start && git clone https://github.com/skywind3000/vim-quickui
```

可选设置 Unicode 边框：

```vim
let g:quickui_border_style = 2
```

完事了，没有构建步骤，没有依赖。

## 你的第一个对话框

来做一个简单的设置对话框，把下面的代码放到一个函数里：

```vim
function! MySettings()
    let items = [
        \ {'type': 'label', 'text': 'Settings:'},
        \ {'type': 'input', 'name': 'name', 'prompt': 'Name:',
        \  'value': 'test'},
        \ {'type': 'radio', 'name': 'choice', 'prompt': 'Pick:',
        \  'items': ['A', 'B', 'C']},
        \ {'type': 'check', 'name': 'flag',
        \  'text': 'Enable Feature'},
        \ {'type': 'button', 'name': 'confirm',
        \  'items': [' &OK ', ' &Cancel ']},
        \ ]
    let result = quickui#dialog#open(items, {'title': 'Settings'})
    echo result
endfunc
```

执行 `:call MySettings()` 效果如下：

![dialog screenshot](https://skywind3000.github.io/images/p/quickui/dialog2.png)

一个真正的对话框，在 Vim 里，带多个控件。

逐行解释一下：

- **`label`** —— 顶部的静态文本，不可聚焦
- **`input`** —— 带提示标签和默认值的文本输入框
- **`radio`** —— 单选按钮组，只能选一个
- **`check`** —— 复选框，可以切换开关
- **`button`** —— 底部的按钮行

你可以用 `Tab` 和 `Shift-Tab` 在控件间切换焦点，在输入框里直接打字，按 `Space` 切换复选框或选择单选项，按 `Enter` 或点击按钮确认。

所有的值都在 `result` 字典里返回。

## 用户是怎么退出的？

对话框关闭后，你需要知道两件事：用户是确认了还是取消了？如果确认了，是按了按钮还是在输入框里按了回车？

返回值有两个关键字段：

- `button_index` —— 按了哪个按钮（0 起始），取消时为 `-1`
- `button` —— 按钮控件的 name，如果是在非按钮控件上按回车或取消则为 `''`

这是你在每个对话框里都会用到的判断模式：

```vim
let r = quickui#dialog#open(items, opts)

if r.button_index == -1
    " 用户按了 ESC、Ctrl-C 或关闭按钮
    echo 'Cancelled'
elseif r.button == ''
    " 用户在输入框/单选/复选上按了回车
    echo 'Confirmed (Enter): name=' . r.name
else
    " 用户点击了某个按钮
    echo 'Button pressed: ' . r.button . ' #' . r.button_index
endif
```

几个要点：

- **`button_index` 从 0 开始**。第一个按钮返回 `0`，第二个返回 `1`，依此类推。
- **用 `button` 区分回车和按钮点击**。当 `button_index` 为 `0` 时，检查 `r.button`：如果为 `''`，说明是在非按钮控件上按了回车；如果非空，说明是点击了第一个按钮。
- **取消时仍然返回值**。即使按了 ESC，`r.name` 等字段仍然包含用户在取消前输入的内容。下次重新打开对话框时可以恢复状态。

大多数情况下，你只需要这样判断：

```vim
let r = quickui#dialog#open(items, opts)

if r.button_index >= 0 && r.button != ''
    " 用户点击了某个按钮——处理返回值
    echo 'Name: ' . r.name
endif
```

或者如果你有 OK 和 Cancel 两个按钮：

```vim
" ' &OK ' 是按钮 0，' &Cancel ' 是按钮 1
if r.button_index == 0 && r.button != ''
    echo 'Accepted: ' . r.name
endif
```

## 一个实战例子

来做一个更贴近真实插件的东西：一个"新建项目"的表单，包含所有控件类型：

```vim
function! NewProject()
    let items = [
        \ {'type': 'label', 'text': 'Create New Project:'},
        \ {'type': 'input', 'name': 'project_name', 'prompt': 'Project:'},
        \ {'type': 'input', 'name': 'email', 'prompt': 'Email:'},
        \ {'type': 'dropdown', 'name': 'language', 'prompt': 'Language:',
        \  'items': ['Python', 'JavaScript', 'Go', 'Rust', 'C++'],
        \  'value': 0},
        \ {'type': 'dropdown', 'name': 'build', 'prompt': 'Build:',
        \  'items': ['Make', 'CMake', 'Cargo', 'npm', 'pip'],
        \  'value': 0},
        \ {'type': 'radio', 'name': 'license', 'prompt': 'License:',
        \  'items': ['&MIT', '&Apache', '&GPL', '&Proprietary'],
        \  'value': 0},
        \ {'type': 'check', 'name': 'git_init',
        \  'text': 'Initialize git repo', 'value': 1},
        \ {'type': 'check', 'name': 'ci',
        \  'text': 'Add CI config'},
        \ {'type': 'button', 'name': 'confirm',
        \  'items': [' &Create ', '  Cancel  ']},
        \ ]

    let opts = {'title': 'New Project', 'w': 50, 'focus': 'project_name'}
    let result = quickui#dialog#open(items, opts)

    " 检查用户是否点击了 "Create" 按钮（按钮 0）
    if result.button_index == 0 && result.button != ''
        let languages = ['Python', 'JavaScript', 'Go', 'Rust', 'C++']
        let builds = ['Make', 'CMake', 'Cargo', 'npm', 'pip']

        echo 'Project:  ' . result.project_name
        echo 'Email:    ' . result.email
        echo 'Language: ' . languages[result.language]
        echo 'Build:    ' . builds[result.build]
        echo 'License:  ' . result.license
        echo 'Git:      ' . (result.git_init ? 'yes' : 'no')
        echo 'CI:       ' . (result.ci ? 'yes' : 'no')
    else
        echo 'Cancelled'
    endif
endfunc
```

效果截图：

![](https://skywind3000.github.io/images/p/quickui/dialog3.png)

这个例子展示了几个要点：

**下拉列表控件**（dropdown）显示为一个折叠的选择框。按 `Enter` 或 `Space` 弹出选项列表供选择。返回值是 0 起始的索引，需要自己映射回文本。

**分隔线**（separator）在复选框和按钮之间画一条水平线，替代了控件间的默认空行，保持布局整洁。

**`opts.focus`** 把初始焦点设置到 `project_name` 输入框，用户打开对话框就能立刻开始输入。

**提示文本自动对齐**。注意 `Project:`、`Email:`、`Language:`、`Build:` 和 `License:` 这些标签都是左对齐的，它们后面的控件起始位置在同一列。QuickUI 会自动计算最长的提示文本，补齐其余的。

**热键标记**。按钮、单选和复选文本中的 `&` 标记了热键字符。比如 `&Create` 让 `C` 成为热键——在对话框的任何地方（不在输入框中时）按 `C` 就能触发该按钮。单选组的 `&MIT`、`&Apache` 等同理。

## 使用技巧

分享几个我在开发对话框过程中总结的经验：

**先设好 `opts.w`。** 如果不设宽度，QuickUI 会自动计算。对于简单对话框没问题，但对于有多个字段的表单，显式设置一个宽度（比如 `50`）能让布局更一致。

**用 `'value'` 设默认值。** 每个控件都支持 `value` 字段。输入框接收字符串，单选/下拉/复选框接收数字。预填好默认值能让用户少打几个字。

**复选框不需要提示标签。** 和输入框、单选不同，复选框的文本本身就是标签，不加 `prompt` 看着更自然。如果想让它和其他有提示的控件对齐，也可以加 `'prompt'` 字段。

**给按钮行命名。** 如果只有一行按钮，默认名字 `'button'` 就够了。但如果有两行按钮（比如 "Apply/Reset" 和 "OK/Cancel"），要给它们不同的 `name`，这样才能区分用户点的是哪一行。

## 更多进阶特性

本文只覆盖了基础用法。对话框系统还有更多能力：

- **输入历史** —— 输入框可以通过 `history` 字段在多次调用间共享历史记录，按 `Ctrl+Up` / `Ctrl+Down` 浏览
- **垂直单选** —— 选项文本较长时，单选组会自动切换为垂直布局
- **表单验证** —— 通过 `opts.validator` 设置一个回调函数，在对话框关闭前验证字段值
- **鼠标支持** —— 点击任何控件即可聚焦、切换或激活
- **自定义颜色和边框** —— 配合你的 Vim 配色方案

完整参考可查看 vim-quickui 仓库中的 [Dialog Guide](https://github.com/skywind3000/vim-quickui/blob/master/DIALOG.md)。

## 不只是对话框

vim-quickui 不仅仅是对话框。它还提供：

- **顶部菜单栏** —— 屏幕顶部的下拉菜单，Borland/Turbo C++ 风格
- **右键菜单** —— 光标附近弹出的上下文菜单
- **列表框** —— 带搜索功能的可滚动列表
- **文本框** —— 在弹出窗口中显示文本
- **预览窗口** —— 在光标附近预览文件内容
- **输入框** —— 简单的单行输入（比完整对话框轻量）
- **终端** —— 在弹出窗口中运行 shell 命令

全部是纯 VimScript 实现，全部同时支持 Vim 和 NeoVim。

详细文档参见：[完整文档](https://github.com/skywind3000/vim-quickui/blob/master/MANUAL.md)

---

如果你觉得 vim-quickui 有用，欢迎去 [GitHub](https://github.com/skywind3000/vim-quickui) star 一下，也帮助更多人发现这个项目。

有问题或想法？欢迎提 [issue](https://github.com/skywind3000/vim-quickui/issues) 或者在下面评论。
