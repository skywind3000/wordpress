---
uuid: 1690
title: 更好的使用 Vim 标签（Tab）来切换文件
status: publish
categories: 随笔
tags: Vim
slug: 
date: 2016-05-03 07:19
---
更好的使用 Vim7.0 以后推出的标签（TAB）功能，同现代编辑器一样用标签（TAB）来管理多文件，代替传统 Buffer List：

![](https://skywind3000.github.io/images/blog/wp-content/2016/05/vim3.png)

让 Minibufexplor/tabbar 这些上个世纪的插件都退场吧，直接使用标准的标签功能会更加舒服。

#### 快捷键切换 TAB

第一件事情就是要搞定标签快速切换问题，不管是 `:tabn X` 还是 `Xgt` 都十分低效，我们需要更快速的在各个文件之间切换。最简单的是设置 0-9 来快速切换 tab（默认 leader 是反斜杠，即先按下 `\` 键，再按数字键），不管终端还是 GVIM 都兼容：

```vim
noremap <silent><tab>m :tabnew<cr>
noremap <silent><tab>e :tabclose<cr>
noremap <silent><tab>n :tabn<cr>
noremap <silent><tab>p :tabp<cr>
noremap <silent><leader>t :tabnew<cr>
noremap <silent><leader>g :tabclose<cr>
noremap <silent><leader>1 :tabn 1<cr>
noremap <silent><leader>2 :tabn 2<cr>
noremap <silent><leader>3 :tabn 3<cr>
noremap <silent><leader>4 :tabn 4<cr>
noremap <silent><leader>5 :tabn 5<cr>
noremap <silent><leader>6 :tabn 6<cr>
noremap <silent><leader>7 :tabn 7<cr>
noremap <silent><leader>8 :tabn 8<cr>
noremap <silent><leader>9 :tabn 9<cr>
noremap <silent><leader>0 :tabn 10<cr>
noremap <silent><s-tab> :tabnext<CR>
inoremap <silent><s-tab> <ESC>:tabnext<CR>
```

其次，GVIM/MacVim 下设置 ALT-0-9 来切换TAB：

```vim
" keymap to switch table in gui
if has('gui_running') 
    set winaltkeys=no
    set macmeta
    noremap <silent><c-tab> :tabprev<CR>
    inoremap <silent><c-tab> <ESC>:tabprev<CR>
    noremap <silent><m-1> :tabn 1<cr>
    noremap <silent><m-2> :tabn 2<cr>
    noremap <silent><m-3> :tabn 3<cr>
    noremap <silent><m-4> :tabn 4<cr>
    noremap <silent><m-5> :tabn 5<cr>
    noremap <silent><m-6> :tabn 6<cr>
    noremap <silent><m-7> :tabn 7<cr>
    noremap <silent><m-8> :tabn 8<cr>
    noremap <silent><m-9> :tabn 9<cr>
    noremap <silent><m-0> :tabn 10<cr>
    inoremap <silent><m-1> <ESC>:tabn 1<cr>
    inoremap <silent><m-2> <ESC>:tabn 2<cr>
    inoremap <silent><m-3> <ESC>:tabn 3<cr>
    inoremap <silent><m-4> <ESC>:tabn 4<cr>
    inoremap <silent><m-5> <ESC>:tabn 5<cr>
    inoremap <silent><m-6> <ESC>:tabn 6<cr>
    inoremap <silent><m-7> <ESC>:tabn 7<cr>
    inoremap <silent><m-8> <ESC>:tabn 8<cr>
    inoremap <silent><m-9> <ESC>:tabn 9<cr>
    inoremap <silent><m-0> <ESC>:tabn 10<cr>
endif
```

或者在 MacVim 下还可以用 CMD_0-9 快速切换，按着更舒服：

```vim
if has("gui_macvim")
    set macmeta
    noremap <silent><c-tab> :tabprev<CR>
    inoremap <silent><c-tab> <ESC>:tabprev<CR>
    noremap <silent><d-1> :tabn 1<cr>
    noremap <silent><d-2> :tabn 2<cr>
    noremap <silent><d-3> :tabn 3<cr>
    noremap <silent><d-4> :tabn 4<cr>
    noremap <silent><d-5> :tabn 5<cr>
    noremap <silent><d-6> :tabn 6<cr>
    noremap <silent><d-7> :tabn 7<cr>
    noremap <silent><d-8> :tabn 8<cr>
    noremap <silent><d-9> :tabn 9<cr>
    noremap <silent><d-0> :tabn 10<cr>
    inoremap <silent><d-1> <ESC>:tabn 1<cr>
    inoremap <silent><d-2> <ESC>:tabn 2<cr>
    inoremap <silent><d-3> <ESC>:tabn 3<cr>
    inoremap <silent><d-4> <ESC>:tabn 4<cr>
    inoremap <silent><d-5> <ESC>:tabn 5<cr>
    inoremap <silent><d-6> <ESC>:tabn 6<cr>
    inoremap <silent><d-7> <ESC>:tabn 7<cr>
    inoremap <silent><d-8> <ESC>:tabn 8<cr>
    inoremap <silent><d-9> <ESC>:tabn 9<cr>
    inoremap <silent><d-0> <ESC>:tabn 10<cr>
    noremap <silent><d-o> :browse tabnew<cr>
    inoremap <silent><d-o> <ESC>:browse tabnew<cr>
endif
```

这下很舒服了，和大部分主流编辑器一样切换tab十分轻松。那终端下 alt没法很好的映射怎么办呢？

#### 终端下映射 ALT-0-9 快速切换标签

不推荐把中断里的 ALT 键设置成 ESC+，大部分终端（XShell, SecureCRT, iTerm, gnome-terminal）都提供 ALT 键改为 ESC+ 的模式，即按下 `ALT-A`，终端会连续发送 `ESC(27)` 和 `A(65)` 两个字节，正确设置见：

[终端里正确设置 ALT 键和 BS 键](/blog/archives/2021)

不需要 ALT 键的话可以继续往下。

#### 设置标签文本

默认的标签文本包含文件路径，十分凌乱，需要进一步修改，让它只显示文件名：

```vim
" make tabline in terminal mode
function! Vim_NeatTabLine()
    let s = ''
    for i in range(tabpagenr('$'))
        " select the highlighting
        if i + 1 == tabpagenr()
            let s .= '%#TabLineSel#'
        else
            let s .= '%#TabLine#'
        endif
        " set the tab page number (for mouse clicks)
        let s .= '%' . (i + 1) . 'T'
        " the label is made by MyTabLabel()
        let s .= ' %{Vim_NeatTabLabel(' . (i + 1) . ')} '
    endfor
    " after the last tab fill with TabLineFill and reset tab page nr
    let s .= '%#TabLineFill#%T'
    " right-align the label to close the current tab page
    if tabpagenr('$') > 1
        let s .= '%=%#TabLine#%999XX'
    endif
    return s
endfunc

" get a single tab name 
function! Vim_NeatBuffer(bufnr, fullname)
    let l:name = bufname(a:bufnr)
    if getbufvar(a:bufnr, '&modifiable')
        if l:name == ''
            return '[No Name]'
        else
            if a:fullname 
                return fnamemodify(l:name, ':p')
            else
                return fnamemodify(l:name, ':t')
            endif
        endif
    else
        let l:buftype = getbufvar(a:bufnr, '&buftype')
        if l:buftype == 'quickfix'
            return '[Quickfix]'
        elseif l:name != ''
            if a:fullname 
                return '-'.fnamemodify(l:name, ':p')
            else
                return '-'.fnamemodify(l:name, ':t')
            endif
        else
        endif
        return '[No Name]'
    endif
endfunc

" get a single tab label
function! Vim_NeatTabLabel(n)
    let l:buflist = tabpagebuflist(a:n)
    let l:winnr = tabpagewinnr(a:n)
    let l:bufnr = l:buflist[l:winnr - 1]
    return Vim_NeatBuffer(l:bufnr, 0)
endfunc

" get a single tab label in gui
function! Vim_NeatGuiTabLabel()
    let l:num = v:lnum
    let l:buflist = tabpagebuflist(l:num)
    let l:winnr = tabpagewinnr(l:num)
    let l:bufnr = l:buflist[l:winnr - 1]
    return Vim_NeatBuffer(l:bufnr, 0)
endfunc

" setup new tabline, just like %M%t in macvim
set tabline=%!Vim_NeatTabLine()
set guitablabel=%{Vim_NeatGuiTabLabel()}
```

在 GUI 模式下，还可以配置标签的 TIPS，鼠标移动到标签上，会自动显示该 TIPS：

```vim
" get a label tips
function! Vim_NeatGuiTabTip()
    let tip = ''
    let bufnrlist = tabpagebuflist(v:lnum)
    for bufnr in bufnrlist
        " separate buffer entries
        if tip != ''
            let tip .= " \n"
        endif
        " Add name of buffer
        let name = Vim_NeatBuffer(bufnr, 1)
        let tip .= name
        " add modified/modifiable flags
        if getbufvar(bufnr, "&modified")
            let tip .= ' [+]'
        endif
        if getbufvar(bufnr, "&modifiable")==0
            let tip .= ' [-]'
        endif
    endfor
    return tip
endfunc
set guitabtooltip=%{Vim_NeatGuiTabTip()}
```

#### 快速在标签中打开文件

除了 `:tabedit` 外，Vim 自带 netrw 插件可以浏览目录，是代替 nerdtree 的好东西，使用 `:Explore` 打开 netrw 的文件浏览器后，选中文件按t键即可以再新标签打开对应文件了。

#### 快捷键在标签打开新文件

我们配置按下 ALT-O 的时候在当前位置打开文件浏览器：

```vim
" Open Explore in new tab with current directory
function! Open_Explore(where)
    let l:path = expand("%:p:h")
    if l:path == ''
        let l:path = getcwd()
    endif
    if a:where == 0
        exec 'Explore '.fnameescape(l:path)
    elseif a:where == 1
        exec 'vnew'
        exec 'Explore '.fnameescape(l:path)
    else
        exec 'tabnew'
        exec 'Explore '.fnameescape(l:path)
    endif
endfunc
```

这样可以把 call Open_Explore(2) 映射成 ALT-O，这样如果在编辑一个文件时候按下 ALT-O，那么会在该文件的路径下展开一个新的 tab 并显示 netrw 的文件列表。

如果使用 GVIM/MacVim 可以更优雅点，直接在当前文件的路径下，使用系统的文件查找窗口，选中文件后在新的 Tab 里打开：

```vim
function! s:Filter_Push(desc, wildcard)
    let g:browsefilter .= a:desc . " (" . a:wildcard . ")\t" . a:wildcard . "\n"
endfunc

let g:browsefilter = ''
call s:Filter_Push("All Files", "*")
call s:Filter_Push("C/C++/Object-C", "*.c;*.cpp;*.cc;*.h;*.hh;*.hpp;*.m;*.mm")
call s:Filter_Push("Python", "*.py;*.pyw")
call s:Filter_Push("Text", "*.txt")
call s:Filter_Push("Vim Script", "*.vim")

function! Open_Browse(where)
    let l:path = expand("%:p:h")
    if l:path == '' | let l:path = getcwd() | endif
    if exists('g:browsefilter') && exists('b:browsefilter')
        if g:browsefilter != ''
            let b:browsefilter = g:browsefilter
        endif
    endif
    if a:where == 0
        exec 'browse e '.fnameescape(l:path)
    elseif a:where == 1
        exec 'browse vnew '.fnameescape(l:path)
    else
        exec 'browse tabnew '.fnameescape(l:path)
    endif
endfunc
```

然后把 call Open_Browse(2) 映射成 ALT-O。

#### 寻找Tag时在新标签打开

以前寻找tag时使用 `<C-]>` ，现在改为 `<c-w><c-]>` 即可在新标签打开 tag 定义。

#### Quickfix 中在新标签打开文件

编译或者 grep 的时候，信息输出到 Quickfix 窗口中，按回车就容易把 buf 给切换走，使用标签后设置下面一项，即可更改 quickfix 行为为：如果有已打开文件，先复用，没有的话使用标签：

```vim
set switchbuf=useopen,usetab,newtab
```

如此Tab已经很好用了，再配置一些快捷键按 `ALT-方向键` 来 tabmove，`ALT-w` 来关闭标签，基本上和其他现代编辑器行为很类似了。