---
uuid: 3114
title: 我在命令行下剪辑视频
status: publish
categories: 随笔
tags: 命令行
slug: 
date: 2021-02-09 16:19
---
是的，你不需要格式工厂，你也不需要会声会影，更不需要爱剪辑这些莫名其妙的流氓软件，命令行下视频处理，包括剪辑，转码，提取，合成，缩放，字幕，特效等等，全部命令行搞定，这不是疯狂，而是效率：

#### MP4 转换 GIF

知乎可以发 MP4，但对桌面录屏这种十多二十秒的小短片远远没有 GIF 来的便捷，GIF 在很多软件里支持的也比 MP4 要广泛，转换命令为：

```bash
ffmpeg -i in.mp4 -an -c:v gif out.gif
```

参数 -i 的指明输入文件 "in.mp4" ，-an 代表禁用音频，-c:v 的意思是指定视频编码为 gif，最后是输出文件名。

那么效率在哪里呢？ 别急，我们写完善点，做个脚本：video_convert_to_gif.cmd

```batch
@echo off
if "%1" == "" goto HELP

set "IN=%1"
set "OUT=%~dpn1.gif"

if "%2" == "" goto NEXT
set "OUT=%2"
:NEXT

call ffmpeg -i "%IN%" -an -c:v gif "%OUT%"
pause
goto END

:HELP
echo usage: video_convert_to_gif ^<input^> [^<output^>]
:END
echo.
```

将上面的脚本完善一下，保存成名为 `video_convert_to_gif.cmd` 的脚本：

![](https://skywind3000.github.io/images/blog/2021/cmd_v1.png)

每次要使用的时候，直接把任何格式的视频文件拖到这个脚本上面去，同级目录下就有了一个 gif 文件了，比你格式工厂修改一半天点点点来的高效多了。

#### 转换为 MP4

最简单写法：

```bash
ffmpeg -i in.wmv -c:v libx264 -c:a aac out.mp4
```

前面输入可以是任意格式的视频文件，用 -c:v 指定视频编码器是 libx264，用 c:a 指定音频编码器是 aac，然后输出 mp4，考虑到某些安卓机可能无法正确播放，完善下：

（点击 more/continue 继续）

<!--more-->

```bash
ffmpeg -i in.wmv -c:v libx264 -c:a aac -pix_fmt yuv420p -vf ^
          "scale=trunc(iw/2)*2:trunc(ih/2)*2" out.mp4
```

在 Windows 的 Bat 文件里，`^` 符号代表换行继续，这里针对部分安卓机只能播放 yuv420 的像素格式的问题，做了一些处理，并且把长宽设置为偶数，否则无法使用 yuv420 格式，完善一下，写成脚本：

```batch
@echo off
if "%1" == "" goto HELP

set "IN=%1"
set "OUT=%~dpn1.mp4"

if "%2" == "" goto NEXT
set "OUT=%2"
:NEXT

call ffmpeg -i "%IN%" -c:v libx264 -c:a aac ^
	-pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" ^
   	"%OUT%"
pause
goto END

:HELP
echo usage: video_convert_to_mp4 ^<input^> [^<output^>]
:END
echo.
```

保存成 `video_convert_to_mp4.cmd` 用法和上面相同，也是鼠标拖上去就行了。

#### 转换 H.265

和转换 264 类似：

```bash
ffmpeg -i in.mp4 -c:v libx265 -c:a aac ^
	-pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" ^
	out.x265.mp4
```

脚本文件可以照葫芦画瓢，头两行最后用了 ^ 符号，代表命令在下一行继续。

#### GIF 转换 MP4

上面有了 MP4 到 GIF，反过来的话，需要做一些处理，添加一段空白音频，不然有些软件或者网站可能出问题：

```bash
ffmpeg -f lavfi -i anullsrc -i in.gif -c:v libx264 -c:a aac -shortest ^
       -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" out.mp4
```

这里用了 anullsrc 代表空的音频输入，同时加了一个 -shortest 代表多个输入取时间最短的那个，一样照葫芦画瓢做一个脚本文件封装一下即可。

#### MP4 分离音频

将 MP4 的音频分离出来，保存成 mp3 也是比较常见的用法：

```batch
@echo off
if "%1" == "" goto HELP

set "IN=%1"
set "OUT=%~dpn1.mp3"

if "%2" == "" goto NEXT
set "OUT=%2"
:NEXT

call ffmpeg -i "%IN%" -vn -c:a mp3 -ar 48000 -ac 2 "%OUT%"

pause

goto END
:HELP
echo usage: video_extract_audio ^<input^> [^<output^>]
:END
echo.
```

保存成 `video_extract_audio.cmd` 把文件拖上去即可转换。

这里 -vn 的意思是禁用视频，-c:a 指定编码为 mp3，-ar 的意思是指定音频采样率为 48000，同时 -ac 的意思是声道数量。

#### 视频裁剪

直接上脚本：

```batch
@echo off
if "%3" == "" goto HELP
set "IN=%1"
set "OUT=%~dpn1_clip%~x1"

if "%4" == "" goto NEXT
set "OUT=%4"
:NEXT

call ffmpeg -i "%IN%" -ss "%2" -to "%3" -c:a copy -c:v copy "%OUT%"
pause
goto END

:HELP
echo usage: video_clip ^<input^> ^<from ^(00:00:00.000^)^> ^<to ^(00:10:00.000^)^> [^<output^>]
:END
echo.
```

指定输入文件，然后从几分几秒到积分几秒即可：

```bash
video_clip in.mp4  00:00:00  00:00:10 out.mp4
```

即可剪辑头 10 秒钟的视频保存成 out.mp4

#### 视频合并

将两段视频合并成一段：

```batch
@echo off
if "%2" == "" goto HELP

set "IN1=%1"
set "IN2=%2"
set "OUT=%~dpn1_%~dpn2_merged.%~x1"

if "%3" == "" goto NEXT
set "OUT=%3"
:NEXT

call ffmpeg -i "%IN1%" -i "%IN2%" ^
	-filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[outv][outa]" ^
   	-map "[outv]" -map "[outa]" "%OUT%"
pause

goto END
:HELP
echo usage: video_concat ^<input1^> ^<input2^> [^<output^>]
:END
echo.
```

#### 区域裁剪

将视频里的一个矩形截取出来，保存成一个新的视频：

```batch
@echo off
if "%5" == "" goto HELP

set "IN=%1"
set "OUT=%~dpn1_crop%~x1"

if "%6" == "" goto NEXT
set "OUT=%6"
:NEXT

call ffmpeg -i "%IN%" -filter:v "crop=%4:%5:%2:%3" "%OUT%"
pause

goto END
:HELP
echo usage: video_crop ^<input^> ^<x^> ^<y^> ^<w^> ^<h^> [^<output^>]
:END
echo.
```

这样输入源视频和矩形区域坐标和长宽即可裁剪。

#### 更多用法

欢迎使用 ffmpeg 命令速查表：

- [FFMPEG 命令速查表](https://github.com/skywind3000/awesome-cheatsheets/blob/master/tools/ffmpeg.sh)

附赠：我自己写好的一堆脚本

![](https://skywind3000.github.io/images/blog/2021/cmd_v2.png)

地址：

- [github.com/skywind3000/vim](https://github.com/skywind3000/vim/tree/master/tools/script)

--
