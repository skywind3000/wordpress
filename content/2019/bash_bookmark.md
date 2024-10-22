---
uuid: 3077
title: 十行代码实现命令行书签
status: publish
categories: 编程技术
tags: 命令行,Linux
slug: 
date: 2019-02-06 10:32
---
路径书签/别名，用来给目录取个名字，要用时快速跳转，它不是用来代替：z.lua / z.sh / autojump 这类第一梯队的 cd 辅助工具的，而是作为他们的一个补充。

先前我想找个现成的路径书签的小插件，找到这个：[pm](https://github.com/Angelmmiguel/pm)

把现有目录添加成书签要：

```bash
pm add my-project
```

跳到这个书签对应的目录要：

```bash
pm go my-project
```

然后列出所有书签要：

```bash
pm list
```

删除书签要：

```bash
pm remove my-project
```

我又看了好几个书签软件，都大同小异，又难用，实现又啰嗦，这玩意儿居然写出 500 行以上的代码来，真是匪夷所思。所以我打算用十行代码实现一个更优雅的书签功能。

#### 目标1：少打字

同样一个功能多打一个字母，做一千次就多打了 1K 的内容，能省则省，我不明白为什么这些插件做的都那么啰嗦，输入完命令名还得再输入 add/remove/go/list 之一的参数，然后才是书签名，要我来做，我会把命令名起短一点，比如叫做 m ：

```bash
m         # 列出当前所有书签
m foo     # 跳转到名为 foo 的标签
m +foo    # 将当前路径添加成书签 foo
m -foo    # 删除名为 foo 书签
m /foo    # 搜索名称里包含 foo 的书签
```

大部分时候都频率最高的就是 “跳转” 和 “列出所有书签”，所以尽可能的减少他们输入的字符数，m foo 就是跳转到名字为 foo 的书签，比 pm go foo 少打四个字符，m 后面没参数，就是列出所有书签，pm list 少打六个字符。

其他几项功能也比 pm 少打很多字，用 +/- 三个符号代表：增加，搜索和删除，也很直白。

#### 目标2：代码少

我实在不明白一个简单的插件为什么会写成 500-600 行的翔。我们充分利用 shell 的功能，那么把当前目录添加到书签，就是：

```bash
ln -snf "$(pwd)" "$MARKPATH/$1" 
```

其中 `$MARKPATH` 指向 ~/.local/share/marks 之类的地方，可以自定义，添加书签就是在 `$MARKPATH` 下面做一个软连接，指向当前目录即可。

删除书签：

```bash
rm -i "$MARKPATH/$1" 
```

删除书签就是删除软连接，还会用 rm 命令的 -i 参数问下你是否真的要删除。

跳转书签：

```bash
cd -P "$MARKPATH/$1"
```

不就完了？使用 -P 参数跳转到实际路径，搞那么多花花绕干嘛？

其他的搜索书签就是 find 命令，列出书签就是 ls 命令格式化一下。

#### 实际代码

实际代码用 case 来判断参数前缀，增加了一些边际情况处理，保存成 `m.sh`：

（点击 more/continue 继续）

<!--more-->

```bash
function m() {
    MARKPATH="${MARKPATH:-$HOME/.local/share/marks}"
    [ -d "$MARKPATH" ] || mkdir -p -m 700 "$MARKPATH" 2> /dev/null
    case "$1" in
        +*)            # m +foo  - add new bookmark for $PWD
            ln -snf "$(pwd)" "$MARKPATH/${1:1}" 
            ;;
        -*)            # m -foo  - delete a bookmark named "foo"
            rm -i "$MARKPATH/${1:1}" 
            ;;
        /*)            # m /bar  - search bookmarks matching "bar"
            find "$MARKPATH" -type l -name "*${1:1}*" | \
                awk -F "/" '{print $NF}' | MARKPATH="$MARKPATH" xargs -I'{}'\
                sh -c 'echo "{} ->" $(readlink "$MARKPATH/{}")'
            ;;
        "")            # m       - list all bookmarks
            command ls -1 "$MARKPATH/" | MARKPATH="$MARKPATH" xargs -I'{}' \
                sh -c 'echo "{} ->" $(readlink "$MARKPATH/{}")'
            ;;
        *)             # m foo   - cd to the bookmark directory
            local dest="$(readlink "$MARKPATH/$1" 2> /dev/null)"
            [ -d "$dest" ] && cd "$dest" || echo "No such mark: $1"
            ;;
    esac
}
```

就是这么简短，是用的时候在你的 .bashrc / .zshrc 中添加一下：

```bash
source /path/to/m.sh
```

就能用 m foo 进行跳转，m 列出所有书签，m +foo 添加书签了。懒得多弄一个 m.sh 的话，还可以直接把这个函数帖到你的 rc 文件或者 init.sh 里面。


#### 增加补全

上面提到的好几个书签插件都没做补全，咱们代码量虽少，补全方面也不含糊：

```bash
if [ -n "$BASH_VERSION" ]; then
    function _cdmark_complete() {
        local MARKPATH="${MARKPATH:-$HOME/.local/share/marks}"
        local curword="${COMP_WORDS[COMP_CWORD]}"
        if [[ "$curword" == "-"* ]]; then
            COMPREPLY=($(find "$MARKPATH" -type l -name "${curword:1}*" \
                2> /dev/null | awk -F "/" '{print "-"$NF}'))
        else
            COMPREPLY=($(find "$MARKPATH" -type l -name "${curword}*" \
                2> /dev/null | awk -F "/" '{print $NF}'))
        fi
    }
    complete -F _cdmark_complete m
elif [ -n "$ZSH_VERSION" ]; then
    function _cdmark_complete() {
        local MARKPATH="${MARKPATH:-$HOME/.local/share/marks}"
        if [[ "${1}${2}" == "-"* ]]; then
            reply=($(command ls -1 "$MARKPATH" 2> /dev/null | \
                awk '{print "-"$0}'))
        else
            reply=($(command ls -1 "$MARKPATH" 2> /dev/null))
        fi
    }
    compctl -K _cdmark_complete m
fi
```

该补全代码写的稍微啰嗦了点，但是主要是同时兼容 bash/zsh，有了这些补全代码，你输入完 m 命令后按 tab ，能帮你补全书签名称。

好了，前后代码加起来，不超过 50 行，比其他那些 400-500 行的垃圾插件优雅多了。

所以说，灵活应用各类终端工具，玩得转 awk/xargs/sed 等，就能让你事半功倍。

